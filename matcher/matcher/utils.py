# coding: utf-8

import ast
import os


import pandas as pd

from matcher import ioutils

from . import  api


# load dotenv
from dotenv import load_dotenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

# load environment variables
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


def concatenate_person_index(df:pd.DataFrame) -> pd.Series:
    person_column_names = KEYS
    person_df = df[person_column_names]
    return person_df.apply(lambda x: ''.join(x.map(str)), axis=1)


def get_matched_table_name(jurisdiction:str, event_type:str) -> str:
    return f'matched.{jurisdiction}_{event_type}'


def join_matched_and_merged_data(right_df:pd.DataFrame, jurisdiction:str, event_type:str) -> pd.DataFrame:
    left_df=ioutils.read_merged_data_from_s3(jurisdiction, event_type)

    cols_to_use = right_df.columns.difference(left_df.columns).values

    df = left_df.merge(
        right=right_df[cols_to_use],
        left_index=True,
        right_index=True,
        copy=False,
        validate='many_to_one'
    )
    api.app.logger.info(f'Joined match ids to merged data for {jurisdiction}')

    return df


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

