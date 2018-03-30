# coding: utf-8

import ast
import os
import subprocess


import numpy as np
import pandas as pd
from io import StringIO
import boto3
import psycopg2
import smart_open
import botocore


import matcher.api as api


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
    # index_column_names = INDEXES[event_type]
    index_column_names = KEYS
    index_columns = df[index_column_names]
    return index_columns.apply(lambda x: ''.join(x.map(str)), axis=1)


def read_merged_data_from_s3(jurisdiction:str, event_type:str) -> pd.DataFrame:
    # Read the data in and select the necessary columns
    api.app.logger.info(f"Reading data from {S3_BUCKET}/{jurisdiction}/{event_type}")
    merged_key = f'csh/matcher/{jurisdiction}/{event_type}/merged'
    df=pd.read_csv(f's3://{S3_BUCKET}/{merged_key}', sep='|')
 
    df['source_index'] = concatenate_source_index(df, event_type)
    df.set_index('source_index', drop=True, inplace=True)

    return df


def get_matched_table_name(jurisdiction:str, event_type:str) -> str:
    return f'{jurisdiction}_{event_type}_matched'

def write_matched_data(df:pd.DataFrame, jurisdiction:str, event_type:str):
    api.app.logger.info(f'Writing matched data for {jurisdiction} {event_type}')
    df = df[df.event_type == event_type]

    right_df=read_merged_data_from_s3(jurisdiction, event_type)

    cols_to_use = right_df.columns.difference(df.columns).values

    df = df.merge(
        right=right_df[cols_to_use],
        left_index=True,
        right_index=True,
        copy=False,
        validate='one_to_many'
    )
    
    key = f'csh/matcher/{jurisdiction}/{event_type}/matched'
    write_to_s3(df,key)
    api.app.logger.info(f'Written data for {jurisdiction} {event_type} to S3.')
    write_matched_data_to_postgres(
        key=key, 
        table_name=get_matched_table_name(jurisdiction, event_type), 
        column_names=df.columns.values
    )
    api.app.logger.info(f'Written data for {jurisdiction} {event_type} to postgres.')


def select_columns(df:pd.DataFrame, keys:list) -> pd.DataFrame:
    """ 
    Reduces the dataframe to the columns selected for matching.
    
    We always expect at least two columns: source and source_id
    """
    api.app.logger.info(f'Selecting columns for matching.')
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

    api.app.logger.info(f'Creating table matched.{table_name}')
    col_list = [f'{col} varchar' for col in column_names]
    col_type_list = ', '.join(col_list)
    create_table_query = f"""
        CREATE SCHEMA IF NOT EXISTS matched;
        DROP TABLE IF EXISTS matched.{table_name};
        CREATE TABLE matched.{table_name} (
            {col_type_list}
        );
    """
    api.app.logger.warning(create_table_query)
    cur.execute(create_table_query)

    api.app.logger.info(f'Inserting data into matched.{table_name}')
    with smart_open.smart_open(f's3://{S3_BUCKET}/{key}') as f:
        copy_query = f"""
            COPY matched.{table_name} FROM STDIN WITH CSV HEADER DELIMITER AS '|'
        """
        cur.copy_expert(
            sql=copy_query,
            file=f
        )
    conn.commit()
    api.app.logger.info(f'Done writing matched results to matched.{table_name}')

    cur.close()
    conn.close()


def write_to_s3(df, key):
    api.app.logger.info(f'Writing data to s3://{S3_BUCKET}/{key}')
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, sep='|', index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(S3_BUCKET, key).put(Body=csv_buffer.getvalue())


