# coding: utf-8

import os
import subprocess
import logging

import pandas as pd
import boto3
import botocore


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
    event_type:str,
    timestamp:str=None
) -> pd.DataFrame:
    """
    Given a bucket, jurisdiction, & event type, download the merged data file from S3.
    """
    # setup
    s3 = boto3.client('s3')
    key = f'matcher/{jurisdiction}/{event_type}/merged'
    
    # try to download & return the file, provide feedback or raise error if fails
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        return(pd.read_csv(obj['Body'], sep='|'))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
        logging.warning("The merged data file does not exist.")
    else:
        raise


def version(df:pd.DataFrame) -> pd.DataFrame:
    """
    Adds the code version (git head hash) to the passed DataFrame.
    """
    head_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).rstrip()
    df['code_version'] = head_hash
    
    return df
