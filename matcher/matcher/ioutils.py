# coding: utf-8

import os
from os.path import dirname

import pandas as pd
import s3fs
import yaml
from urllib.parse import urlparse
from contextlib import contextmanager
from retrying import retry

from matcher.logger import logger
from matcher import  utils

# load dotenv
from dotenv import load_dotenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


@retry(stop_max_delay=15000, wait_fixed=3000)
@contextmanager
def open_sesame(path, *args, **kwargs):
    """Opens files either on s3 or a filesystem according to the path's scheme

    Uses s3fs so boto3 is used.
    This means mock_s3 can be used for tests, instead of the mock_s3_deprecated
    """
    path_parsed = urlparse(path)
    scheme = path_parsed.scheme  # If '' or 'file' then a regular file; if 's3' then 's3'

    if not scheme or scheme == 'file':  # Local file
        os.makedirs(dirname(path), exist_ok=True)
        with open(path, *args, **kwargs) as f:
            yield f
    elif scheme == 's3':
        s3 = s3fs.S3FileSystem()
        with s3.open(path, *args, **kwargs) as f:
            yield f


def load_data_for_matching(base_data_directory:str, event_types:list, keys:list, match_job_id:str) -> list:
    # We will frame the record linkage problem as a deduplication problem
    logger.debug(f'Loading data for event types: {event_types}')
    try:
        df = pd.concat([load_one_event_type(base_data_directory, event_type, keys, match_job_id) for event_type in event_types])
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
    df = df.drop_duplicates(subset=keys)

    logger.debug(f"The loaded dataframe has the following columns: {df.columns}")
    logger.debug(f"The dimensions of the loaded dataframe is: {df.shape}")
    logger.debug(f"The indices of the loaded dataframe are {df.index}")
    logger.debug(f'The loaded has {len(df)} rows and {len(df.index.unique())} unique indices')
    logger.debug(f'The loaded dataframe has the following duplicate indices: {df[df.index.duplicated()].index.values}')

    # Cache read data
    write_dataframe(df=df.reset_index(), filepath=f'{base_data_directory}/match_cache/loaded_data/{match_job_id}')

    return df, event_types_read


def load_one_event_type(base_data_directory:str, event_type:str, keys:list, match_job_id:str) -> pd.DataFrame:
    logger.info(f'Loading {event_type} data for matching from {base_data_directory}.')

    try:
        df = read_merged_data(base_data_directory, event_type, keys)

        # Dropping columns that we don't need for matching
        df = df[keys]

        # Keeping track of the event_type
        df['event_type'] = event_type

        logger.info(f'{event_type} data loaded from S3.')

        return df

    except FileNotFoundError as e:
        logger.info(f'No merged file found for {event_type} in {base_data_directory}. Skipping.')
        pass


def read_merged_data(base_data_directory:str, event_type:str, keys:list) -> pd.DataFrame:
    # Read the data in and select the necessary columns
    merged_filepath = f'{base_data_directory}/{event_type}/merged'
    logger.info(f"Reading data from {merged_filepath}")
    df = pd.read_csv(merged_filepath, sep='|')

    df['person_index'] = utils.concatenate_person_index(df, keys)
    df.set_index('person_index', drop=True, inplace=True)

    return df


def write_matched_data(
    matches:pd.DataFrame,
    base_data_directory:str,
    person_keys:list,
    schema_pk_lookup:dict,
    match_job_id:str
) -> dict:
    write_dataframe(df=matches.reset_index(), filepath=f'{base_data_directory}/match_cache/matcher_results/{match_job_id}')
    matched_results_paths = {}
    logger.debug(schema_pk_lookup)
    for event_type, primary_keys in schema_pk_lookup.items():
        logger.info(f'Writing matched data for {base_data_directory} {event_type}')
        matched_results_paths[event_type] = write_one_event_type(
            df=matches,
            base_data_directory=base_data_directory,
            event_type=event_type,
            person_keys=person_keys,
            primary_keys=primary_keys,
            match_job_id=match_job_id
        )

    return matched_results_paths


def write_one_event_type(
    df:pd.DataFrame,
    base_data_directory:str,
    event_type:str,
    person_keys:list,
    primary_keys:list,
    match_job_id:str
) -> str:
    # Join the matched ids to the source data
    logger.info(f'Joining matches to merged data for {event_type}')
    df = join_matched_and_merged_data(df, base_data_directory, event_type, person_keys, primary_keys)

    # Cache the current match to S3
    logger.info(f'Writing data for {base_data_directory} {event_type} to S3.')
    write_dataframe(df=df, filepath=f'{base_data_directory}/{event_type}/matches/{match_job_id}')
    write_dataframe(df=df, filepath=f'{base_data_directory}/{event_type}/matched')

    return f'{base_data_directory}/{event_type}/matched'


def join_matched_and_merged_data(
    right_df:pd.DataFrame, 
    base_data_directory:str,
    event_type:str,
    person_keys:list,
    primary_keys:list
) -> pd.DataFrame:
    left_df=read_merged_data(base_data_directory, event_type, person_keys)[primary_keys]

    df = left_df.merge(
        right=right_df['matched_id'].to_frame(),
        left_index=True,
        right_index=True,
        copy=False,
        validate='many_to_one'
    )
    logger.info(f'Joined match ids to merged data for {event_type}')

    return df


def write_dataframe(df:pd.DataFrame, filepath:str) -> None:
    with open_sesame(filepath, 'wb') as fout:
        fout.write(df.to_csv(sep='|', index=False).encode())

    logger.info(f'Wrote data to {filepath}')


def write_dict_to_yaml(dict_to_write:dict, filepath:str):
    logger.debug(f'Writing some dictionary data to {filepath}! Oooooo!')
    with open_sesame(filepath, 'wb') as fout:
        fout.write(yaml.dump(dict_to_write).encode())
    logger.info(f'Wrote metadata to {filepath}')

