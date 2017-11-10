# coding: utf-8

import os

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
    data_type:str,
    county:str,
    timestamp:str=None
) -> pd.DataFrame:
    """
    Given a bucket, a datatype, a county, download the merged data file from S3.
    """
    # setup
    s3 = boto3.resource('s3')
    key = '{jurisdiction}/{service_provider}/merged'.format(county, data_type)
    local_filename = 'temp_data.csv'

    # try to download the file, provide feedback or raise error if fails
    try:
        s3.Bucket('csh').download_file(key, local_filename)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
        print("The merged data file does not exist.")
    else:
        raise

    # read in the data, delete the file, and return
    df = pd.read_csv(local_filename)
    os.remove(local_filename)
    return df
