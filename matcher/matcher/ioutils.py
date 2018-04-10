# coding: utf-8

import ast
import os


import pandas as pd
from io import StringIO
import boto3
import psycopg2
import smart_open
import botocore


from matcher.logger import logger

import matcher.utils as utils


# load dotenv
from dotenv import load_dotenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


# load environment variables
S3_BUCKET = os.getenv('S3_BUCKET')
PG_CONNECTION = {
    'host': os.getenv('PGHOST'),
    'user': os.getenv('PGUSER'),
    'dbname': os.getenv('PGDATABASE'),
    'password': os.getenv('PGPASSWORD'),
    'port': os.getenv('PGPORT')
}
KEYS = ast.literal_eval(os.getenv('KEYS'))


# lookups
EVENT_TYPES = [
    'hmis_service_stays',
    'jail_bookings'
]



def load_data_for_matching(jurisdiction:str, upload_id:str) -> tuple:
    # We will frame the record linkage problem as a deduplication problem
    df = pd.concat([load_one_event_type(jurisdiction, event_type, upload_id) for event_type in EVENT_TYPES])

    ## and the upload_id
    df['upload_id'] = upload_id

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
    write_dataframe_to_s3(df=df, key=f'csh/matcher/{jurisdiction}/match_cache/loaded_data/{upload_id}')

    return df, event_types_read


def load_one_event_type(jurisdiction:str, event_type:str, upload_id:str) -> pd.DataFrame:
    logger.info(f'Loading {jurisdiction} {event_type} data for matching.')

    try:
        df = read_merged_data_from_s3(jurisdiction, event_type)

        # Dropping columns that we don't need for matching
        df = utils.select_columns(df=df, keys=KEYS)

        # Keeping track of the event_type
        df['event_type'] = event_type

        logger.info(f'{jurisdiction} {event_type} data loaded from S3.')

        return df

    except FileNotFoundError as e:
        logger.info(f'No merged file found for {jurisdiction} {event_type}. Skipping.')
        pass


def read_merged_data_from_s3(jurisdiction:str, event_type:str) -> pd.DataFrame:
    # Read the data in and select the necessary columns
    merged_key = f'csh/matcher/{jurisdiction}/{event_type}/merged'
    logger.info(f"Reading data from s3://{S3_BUCKET}/{merged_key}")
    df = pd.read_csv(f's3://{S3_BUCKET}/{merged_key}', sep='|')

    df['person_index'] = utils.concatenate_person_index(df)
    df.set_index('person_index', drop=True, inplace=True)

    return df


def write_matched_data(matches:pd.DataFrame, jurisdiction:str, upload_id:str, event_types_read:list) -> None:
    write_dataframe_to_s3(df=matches, key=f'csh/matcher/{jurisdiction}/match_cache/matcher_results/{upload_id}')
    for event_type in event_types_read:
        logger.info(f'Writing matched data for {jurisdiction} {event_type}')
        write_one_event_type(matches, jurisdiction, event_type, upload_id)


def write_one_event_type(df:pd.DataFrame, jurisdiction:str, event_type:str, upload_id:str) -> None:
    # Join the matched ids to the source data
    logger.info(f'Joining matches to merged data for {event_type}')
    df = utils.join_matched_and_merged_data(df, jurisdiction, event_type)

    # Cache the current match to S3
    logger.info(f'Writing data for {jurisdiction} {event_type} to S3.')
    write_dataframe_to_s3(df=df, key=f'csh/matcher/{jurisdiction}/{event_type}/matches/{upload_id}')
    write_dataframe_to_s3(df=df, key=f'csh/matcher/{jurisdiction}/{event_type}/matched')

    # Write the current match to postgres for use by the webapp
    logger.info(f'Writing data for {jurisdiction} {event_type} to postgres.')
    write_matched_data_to_postgres(
        key=f'csh/matcher/{jurisdiction}/{event_type}/matched',
        table_name=utils.get_matched_table_name(jurisdiction, event_type),
        column_names=df.columns.values
    )
    logger.info(f'Finished writing {jurisdiction} {event_type} to posgres.')


def write_dataframe_to_s3(df:pd.DataFrame, key:str) -> None:
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, sep='|', index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(S3_BUCKET, key).put(Body=csv_buffer.getvalue())
    logger.info(f'Wrote data to s3://{S3_BUCKET}/{key}')


def write_matched_data_to_postgres(key:str, table_name:str, column_names:list) -> None:
    conn = psycopg2.connect(**PG_CONNECTION)
    cur = conn.cursor()

    logger.info(f'Creating table {table_name}')
    create_schema_if_not_exists('matched', cur)
    create_matched_table(table_name, column_names, cur)

    logger.info(f'Inserting data into {table_name}')
    insert_data_into_table(key, table_name, cur)

    conn.commit()
    cur.close()
    conn.close()


def create_schema_if_not_exists(schema_name:str, cur) -> None:
    create_schema_query = f'CREATE SCHEMA IF NOT EXISTS {schema_name};'
    logger.debug(f'Create schema query: \n{create_schema_query}')
    cur.execute(create_schema_query)
    logger.info(f'Created schema (if not already present) {schema_name}')


def create_matched_table(table_name:str, column_names:list, cur) -> None:
    col_list = [f'{col} varchar' for col in column_names]
    col_type_list = ', '.join(col_list)
    create_table_query = f"""
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name} (
            {col_type_list}
        );
    """
    logger.debug(f'Create table query: \n{create_table_query}')
    cur.execute(create_table_query)
    logger.info(f'Created table {table_name}')


def insert_data_into_table(key:str, table_name:str, cur) -> None:
    with smart_open.smart_open(f's3://{S3_BUCKET}/{key}') as f:
        copy_query = f"""
            COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER AS '|'
        """
        cur.copy_expert(
            sql=copy_query,
            file=f
        )
    logger.info(f'Wrote data to {table_name}')


def read_data_from_postgres(table_name:str):
    conn = psycopg2.connect(**PG_CONNECTION)
    cur = conn.cursor()

    sql = f"SELECT * FROM {table_name};"
    df = pd.io.sql.read_sql_query(sql, conn)
    logger.info(f'Read data from {table_name}')

    conn.close()

    return df


def insert_info_to_match_log(id:str, upload_id:str, match_start_timestamp, match_complete_timestamp, runtime) -> None:
    conn = psycopg2.connect(**PG_CONNECTION)
    cur = conn.cursor()
    logger.info('Writing to match_log')
    query = f"""
    INSERT INTO public.match_log (id, upload_id, match_start_timestamp, match_complete_timestamp, runtime)
        VALUES ('{id}', '{upload_id}', '{match_start_timestamp}', '{match_complete_timestamp}', '{runtime}');
    """
    cur.execute(query)
    logger.info('Wrote to match_log')
    conn.commit()
    cur.close()
    conn.close()
