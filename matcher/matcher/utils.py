# coding: utf-8

import os

import numpy as np
import pandas as pd

from matcher.logger import logger

from uuid import uuid4


# load dotenv
from dotenv import load_dotenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


def summarize_column(column:pd.Series):
    if np.isnan(column.std()):
        std = None
    else:
        std = float(column.std())
    return {
        'mean': float(column.mean()),
        'median': float(column.median()),
        'min': float(column.min()),
        'max': float(column.max()),
        'std': std
    }


def convert_dict_to_str(d:dict):
    s = str(d)
    s = s.replace("{", "")
    s = s.replace("}", "")
    s = s.replace(" ", "")
    s = s.replace(":", "")
    s = s.replace("'", "")
    return s


def concatenate_person_index(df:pd.DataFrame, person_column_names) -> pd.Series:
    person_df = df[person_column_names]
    return person_df.apply(lambda x: ''.join(x.map(str)), axis=1)


def unpack_blocking_rule(df:pd.DataFrame, column_name:str, position:int) -> pd.Series:
    if position < 0:
        return df[column_name].astype(str).str[position:]
    elif position > 0:
        return df[column_name].astype(str).str[:position]
    else:
        raise ValueError('I cannot split a string at this position: {position}')


def unique_match_job_id():
    return str(uuid4())

