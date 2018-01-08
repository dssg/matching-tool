# coding: utf-8

import subprocess
import logging
logger = logging.getLogger('matcher')

import pandas as pd
from io import StringIO
import boto3


def write_to_s3(df, bucket, key):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, sep='|')
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, key).put(Body=csv_buffer.getvalue())


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


def cartesian(df1:pd.DataFrame, df2:pd.DataFrame=None) -> pd.DataFrame:
    """
    Takes two data sets and generates a new data set that contains the cartesian product of the rows.
    If only one dataset is specified, this function returns a self cross join
    """

    #suffixes = ['_'+s for s in sources]

    if df2 is None:
        df2=df1.copy()

    
    df1['_tmpkey'] = 1
    df2['_tmpkey'] = 1

    

    df = pd.merge(df1, df2, on='_tmpkey', suffixes=['_left', '_right']).drop('_tmpkey', axis=1)
    df.index = pd.MultiIndex.from_product((df1.index, df2.index))
    df1.drop("_tmpkey", axis=1, inplace=True)
    df2.drop("_tmpkey", axis=1, inplace=True)

    return df


def generate_row_ids(df:pd.DataFrame) -> pd.DataFrame:
    df['row_id'] = range(0, len(df))
    
    return df


def version(df:pd.DataFrame) -> pd.DataFrame:
    """
    Adds the code version (git head hash) to the passed DataFrame.
    """
    # head_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).rstrip()
    df['code_version'] = '0.1' #head_hash
    
    return df
