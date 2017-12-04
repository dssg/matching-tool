# coding: utf-8

import subprocess
import logging
import io

import pandas as pd
import boto3


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


def load_data_from_s3(
    bucket:str,
    jurisdiction:str,
    event_type:str
) -> pd.DataFrame:
    """
    Given a bucket, jurisdiction, & event type, download the merged data file from S3.
    """
    # setup
    s3 = boto3.client('s3')
    key = f'csh/matcher/{jurisdiction}/{event_type}/merged'
    
    # return the file as a dataframe
    obj = s3.get_object(Bucket=bucket, Key=key)
    return(pd.read_csv(io.BytesIO(obj['Body'].read()), sep='|'))


def version(df:pd.DataFrame) -> pd.DataFrame:
    """
    Adds the code version (git head hash) to the passed DataFrame.
    """
    # head_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).rstrip()
    df['code_version'] = '0.1' #head_hash
    
    return df
