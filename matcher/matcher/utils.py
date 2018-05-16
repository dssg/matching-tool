# coding: utf-8

import ast
import os


import pandas as pd

from matcher import ioutils

from matcher.logger import logger

from uuid import uuid4


# load dotenv
from dotenv import load_dotenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

# load environment variables
KEYS = ast.literal_eval(os.getenv('KEYS'))


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
    logger.info(f'Joined match ids to merged data for {jurisdiction}')

    return df


def unique_match_id():
    return str(uuid4())

