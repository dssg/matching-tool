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


def load_data_for_matching(jurisdiction, upload_id) --> pd.DataFrame:
    # We will frame the record linkage problem as a deduplication problem
    df = pd.concat([read_event_data_from_s3(jurisdiction, e_type, upload_id, KEYS) for event_type in EVENT_TYPES])
    api.app.logger.debug(f"The loaded dataframe has the following columns: {df.columns}")
    api.app.logger.debug(f"The dimensions of the loaded dataframe is: {df.shape}")
    api.app.logger.debug(f"The indices of the loaded dataframe are {df.index}")
    api.app.logger.debug(f'The loaded has {len(df)} rows and {len(df.index.unique())} unique indices')
    api.app.logger.debug(f'The loaded dataframe has the following duplicate indices: {df[df.index.duplicated()].index.values}')

