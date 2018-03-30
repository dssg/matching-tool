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


def load_data_for_matching(jurisdiction:str, upload_id:str) --> tuple:
    # We will frame the record linkage problem as a deduplication problem
    df = pd.concat([load_one_event_type(jurisdiction, e_type, upload_id) for event_type in EVENT_TYPES])

    ## and the upload_id
    df['upload_id'] = upload_id

    # Which event types did we read successfully?
    event_types_read = df.event_type.values

    ## TODO: Check the definition of keys
    # Drop duplicates, disregarding event type
    df.drop('event_type', inplace=True)
    df = df.drop_duplicates(subset=keys)

    api.app.logger.debug(f"The loaded dataframe has the following columns: {df.columns}")
    api.app.logger.debug(f"The dimensions of the loaded dataframe is: {df.shape}")
    api.app.logger.debug(f"The indices of the loaded dataframe are {df.index}")
    api.app.logger.debug(f'The loaded has {len(df)} rows and {len(df.index.unique())} unique indices')
    api.app.logger.debug(f'The loaded dataframe has the following duplicate indices: {df[df.index.duplicated()].index.values}')

    return df, event_types_read


def load_one_event_type(jurisdiction:str, event_type:str, upload_id:str) -> pd.DataFrame:
    api.app.logger.info(f'Loading {jurisdiction} {event_type} data for matching.')

    try:
        df = read_merged_data_from_s3(jurisdiction, event_type)

        # Dropping columns that we don't need for matching
        df = select_columns(df=df, keys=keys)

        # Keeping track of the event_type
        df['event_type'] = event_type

        api.app.logger.info(f'{jurisdiction} {event_type} data loaded from S3.')

        return df

    except FileNotFoundError as e:
        api.app.logger.info(f'No merged file found for {jurisdiction} {event_type}. Skipping.')
        pass

