# coding: utf-8

import ast
import os


import pandas as pd
from io import StringIO
import boto3
import psycopg2
import smart_open
import botocore
import datetime
import yaml


from matcher.logger import logger
from matcher import  utils


# load dotenv
from dotenv import load_dotenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


# load environment variables
S3_BUCKET = os.getenv('S3_BUCKET')
PG_CONNECTION = {
    'host': os.getenv('POSTGRES_HOST'),
    'user': os.getenv('POSTGRES_USER'),
    'dbname': os.getenv('POSTGRES_DB'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'port': os.getenv('POSTGRES_PORT')
}
KEYS = ast.literal_eval(os.getenv('KEYS'))


def load_data_for_matching(base_input_directory:str, event_types, match_job_id:str):
    # We will frame the record linkage problem as a deduplication problem
    logger.debug(f'Loading data for event types: {event_types}')
    try:
        df = pd.concat([load_one_event_type(base_data_directory, event_type, match_job_id) for event_type in event_types])
    except ValueError as e:
        if str(e) != "All objects passed were None":
            raise
        else:
            logger.debug('Found no events data.')
            raise ValueError(f'No merged data files found for any event type ({event_types}) in {base_data_directory}.')
    logger.debug(f'Number of deduped events: {len(df)}')
    
    ## and the match_job_id
    df['match_job_id'] = match_job_id

    # Which event types did we read successfully?
    event_types_read = df.event_type.drop_duplicates().values

    ## TODO: Check the definition of keys
    # Drop duplicates, disregarding event type
    df = df.drop('event_type', axis=1)
    df = df.drop_duplicates(subset=KEYS)

    logger.debug(f"The loaded dataframe has the following columns: {df.columns}")
    logger.debug(f"The dimensions of the loaded dataframe is: {df.shape}")
    logger.debug(f"The indices of the loaded dataframe are {df.index}")
    logger.debug(f'The loaded has {len(df)} rows and {len(df.index.unique())} unique indices')
    logger.debug(f'The loaded dataframe has the following duplicate indices: {df[df.index.duplicated()].index.values}')

    # Cache read data
    write_dataframe_to_s3(df=df.reset_index(), key=f'csh/matcher/{jurisdiction}/match_cache/loaded_data/{match_job_id}')

    return df, event_types_read


def load_one_event_type(base_data_directory:str, event_type:str, match_job_id:str) -> pd.DataFrame:
    logger.info(f'Loading {event_type} data for matching from {data_directory}.')

    try:
        df = read_merged_data(base_directory, event_type)

        # Dropping columns that we don't need for matching
        df = df[KEYS]

        # Keeping track of the event_type
        df['event_type'] = event_type

        logger.info(f'{jurisdiction} {event_type} data loaded from S3.')

        return df

    except FileNotFoundError as e:
        logger.info(f'No merged file found for {event_type} in {data_directory}. Skipping.')
        pass


def read_merged_data(base_data_directory:str, event_type:str) -> pd.DataFrame:
    # Read the data in and select the necessary columns
    merged_filepath = f'{base_data_directory}/{event_type}/merged'
    logger.info(f"Reading data from {merged_filepath}")
    df = pd.read_csv(merged_filepath, sep='|')

    df['person_index'] = utils.concatenate_person_index(df)
    df.set_index('person_index', drop=True, inplace=True)

    return df


def write_matched_data(matches:pd.DataFrame, base_data_directory:str, schema_pk_lookup:dict, match_job_id:str) -> list:
    write_dataframe_to_s3(df=matches.reset_index(), key=f'csh/matcher/{jurisdiction}/match_cache/matcher_results/{match_job_id}')
    matched_results_paths = []
    for event_type, primary_keys in schema_pk_lookup:
        logger.info(f'Writing matched data for {jurisdiction} {event_type}')
        matched_ruluts_paths.append(write_one_event_type(matches, base_data_directory, event_type, primary_keys, match_job_id))

    return matched_results_paths


def write_one_event_type(df:pd.DataFrame, jurisdiction:str, event_type:str, primary_keys:list, match_job_id:str) -> str:
    # Join the matched ids to the source data
    logger.info(f'Joining matches to merged data for {event_type}')
    df = join_matched_and_merged_data(df, base_data_directory, event_type, primary_keys)

    # Cache the current match to S3
    logger.info(f'Writing data for {jurisdiction} {event_type} to S3.')
    write_dataframe(df=df, filepath=f'{base_data_directory}/{event_type}/matches/{match_job_id}')
    write_dataframe(df=df, filepath=f'{base_data_directory}/{event_type}/matched')

    return f'{base_data_directory}/{event_type}/matched'


def join_matched_and_merged_data(right_df:pd.DataFrame, base_data_directory:str, event_type:str, primary_keys:list) -> pd.DataFrame:
    left_df=ioutils.read_merged_data(base_data_directory, event_type)[primary_keys]

    df = left_df.merge(
        right=right_df['matched_id'],
        left_index=True,
        right_index=True,
        copy=False,
        validate='many_to_one'
    )
    logger.info(f'Joined match ids to merged data for {event_type}')

    return df


def write_dataframe(df:pd.DataFrame, filepath:str) -> None:
    with smart_open.smart_open(filepath, 'wb') as fout:
        fout.write( df.to_csv(sep='|', index=False))

    logger.info(f'Wrote data to {filepath}')


def write_dict_to_yaml(dict_to_write:dict, key:str):
    logger.debug(f'Writing some dictionary data to {key}! Oooooo!')
    yaml_string = yaml.dump(dict_to_write)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(S3_BUCKET, key).put(Body=yaml_string.encode())
    logger.info(f'Wrote data to s3://{S3_BUCKET}/{key}')

