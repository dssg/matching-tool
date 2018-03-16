# coding: utf-8
import os
import subprocess

import logging
logger = logging.getLogger('utils')

import numpy as np
import pandas as pd
from io import StringIO
import boto3
import psycopg2
import smart_open
import botocore


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


# these are the columns that, in combination, are the unique row index for each data type
# we need to be able to match back to the source data on these columns.
# i think the best way to do this may be to concatenate them as a single 
# string as a new column 'source_index' or something every time the data are loaded.
# this way. we can reconnect the matched data to all the columns in the source data
# when we go to write the data.
INDEXES = {
    'jail_bookings': ['internal_event_id', 'booking_number', 'location_date'],
    'booking_aka': ['internal_event_id', 'booking_number'],
    'booking_charges': ['internal_event_id', 'internal_charge_id', 'booking_number', 'charge_position', 'charge_date'],
    'case_charges': ['internal_event_id', 'internal_charge_id', 'case_number', 'charge_position', 'charge_date'],
    'hmis_service_stays': ['internal_event_id', 'client_location_start_date'],
    'hmis_aka': ['internal_event_id', 'project_start_date'],
    'by_name': ['internal_event_id', 'full_name', 'first_name', 'middle_name', 'last_name', 'list_entry_date']
}


def get_source_id(df):
    try:
        return df['matched_id']
    except KeyError:
        pass
    try:
        return df['internal_person_id']
    except KeyError:
        pass
    try:
        return df['inmate_number']
    except:
        raise ValueError('No source id column found')


def concatenate_source_index(df:pd.DataFrame, event_type:str) -> pd.Series:
    index_column_names = INDEXES[event_type]
    index_columns = df[index_column_names]
    return index_columns.apply(lambda x: ''.join(x.map(str)), axis=1)


def read_merged_data_from_s3(jurisdiction:str, event_type:str) -> pd.DataFrame:
    # Read the data in and select the necessary columns
    logger.info(f"Reading data from {S3_BUCKET}/{jurisdiction}/{event_type}")
    merged_key = f'csh/matcher/{jurisdiction}/{event_type}/merged'
    df=pd.read_csv(f's3://{S3_BUCKET}/{merged_key}', sep='|')
 
    return df


def load_data_for_matching(jurisdiction:str, event_type:str, upload_id:str, keys:list) -> pd.DataFrame:
    logger.info(f'Loading {jurisdiction} {event_type} data for matching.')
    
    try:
        df = read_merged_data_from_s3(jurisdiction, event_type)

        df['source_index'] = concatenate_source_index(df, event_type)
        df.set_index('source_index', drop=True)

        ## Dropping columns that we don't need for matching
        df = select_columns(df=df,keys=keys)

        ## keeping track of the event_type
        df['event_type'] = event_type

        ## and the upload_id
        df['upload_id'] = upload_id

        ## TODO: Check the definition of keys
        df = df.drop_duplicates(subset=keys)
        
        logger.info(f'{jurisdiction} {event_type} data loaded from S3.')

        return df
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            logger.info(f'No merged file found for {jurisdiction} {event_type}. Skipping.')
            pass
        else:
            raise


def get_matched_table_name(jurisdiction:str, event_type:str) -> str:
    return f'{jurisdiction}_{event_type}_matched'

def write_matched_data(df:pd.DataFrame, jurisdiction:str, event_type:str):
    logger.info(f'Writing matched data for {jurisdiction} {event_type}')
    df = df[df.event_type == event_type]

    right_df=read_merged_data_from_s3(jurisdiction, event_type)
    right_df['source_index'] = concatenate_source_index(right_df, event_type)

    cols_to_use = np.append(right_df.columns.difference(df.columns).values, 'source_index')

    df = df.merge(
        right=right_df[cols_to_use],
        on='source_index',
        copy=False,
        validate='one_to_one'
    )
    
    key = f'csh/matcher/{jurisdiction}/{event_type}/matched'
    write_to_s3(df,key)
    logger.info(f'Written data for {jurisdiction} {event_type} to S3.')
    write_matched_data_to_postgres(
        key=key, 
        table_name=get_matched_table_name(jurisdiction, event_type), 
        column_names=df.columns.values
    )
    logger.info(f'Written data for {jurisdiction} {event_type} to postgres.')


def select_columns(df:pd.DataFrame, keys:list) -> pd.DataFrame:
    """ 
    Reduces the dataframe to the columns selected for matching.
    
    We always expect at least two columns: source and source_id
    """
    logger.info(f'Selecting columns for matching.')
    columns_to_select = ['source', 'source_id', 'internal_person_id', 'source_index']
    if keys:
        columns_to_select = columns_to_select + keys
    
    return df.reindex(keys, axis="columns")


def read_matched_data_from_postgres(table_name:str):
    conn = psycopg2.connect(**PG_CONNECTION)
    cur = conn.cursor()

    sql = f"SELECT * FROM matched.{table_name};"
    dat = pd.io.sql.read_sql_query(sql, conn)

    conn.close()

    return dat


def write_matched_data_to_postgres(key, table_name, column_names):
    conn = psycopg2.connect(**PG_CONNECTION)
    cur = conn.cursor()

    logger.info(f'Creating table matched.{table_name}')
    col_list = [f'{col} varchar' for col in column_names]
    col_type_list = ', '.join(col_list)
    create_table_query = f"""
        CREATE SCHEMA IF NOT EXISTS matched;
        DROP TABLE IF EXISTS matched.{table_name};
        CREATE TABLE matched.{table_name} (
            {col_type_list}
        );
    """
    logger.warning(create_table_query)
    cur.execute(create_table_query)

    logger.info(f'Inserting data into matched.{table_name}')
    with smart_open.smart_open(f's3://{S3_BUCKET}/{key}') as f:
        copy_query = f"""
            COPY matched.{table_name} FROM STDIN WITH CSV HEADER DELIMITER AS '|'
        """
        cur.copy_expert(
            sql=copy_query,
            file=f
        )
    conn.commit()
    logger.info(f'Done writing matched results to matched.{table_name}')

    cur.close()
    conn.close()


def write_to_s3(df, key):
    logger.info(f'Writing data to s3://{S3_BUCKET}/{key}')
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, sep='|', index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, key).put(Body=csv_buffer.getvalue())


