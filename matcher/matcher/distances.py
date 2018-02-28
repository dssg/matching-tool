# coding: utf-8


import pandas as pd
import numpy as np

from typing import List

# String distances

def exact(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    """
    Calculates the "exact distance" between all the selected columns
    """

    for col in keys:
        df[f"distance_in_{col}"] = df.loc[:, df.columns.str.startswith(col)].apply(lambda row: row[0] == row[1], axis = 1)
     
    return df

def truncate_strings(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    return df

def longest_common_substring(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    return df

def levenshtein(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    return df

def qgram(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    return df

def jaccard(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    return df

def jaro_winkler(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    return df


# Numerical distances

def mad(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    return df

def linear_partial_aggrement(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    return df

def quadratic_partial_aggrement(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    return df


# Date distances
