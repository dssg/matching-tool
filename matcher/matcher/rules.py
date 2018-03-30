# coding: utf-8

import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

def exact(df:pd.DataFrame) -> pd.DataFrame:
    """
    Checks if the two rows are an exact match. The result will be stored in the column "matches"
    """

    df["matches"] = df.loc[:, df.columns.str.startswith("exact_distance_in")].apply(lambda row: np.all(row), axis=1)

    return df


def compactify(df:pd.DataFrame, operation='sum', reverse=True) -> pd.DataFrame:

    if operation == 'sum':
        df["matches"] = df.apply(lambda row: np.sum(row), axis=1)
    elif operation == 'norm':
        df["matches"] = df.apply(lambda row: np.linalg.norm(row), axis=1)
    elif operation == 'mean':
        df['matches'] = df.apply(lambda row: np.mean(row), axis=1)
    else:
        print(f"Operation {operation} not supported")
        df["matches"] = np.nan
    
    if reverse:
        df['matches'] = 1 - df['matches']

    return df


def scale(df:pd.DataFrame, score_column='matches', min=0, max=1) -> pd.DataFrame:
    scaler = MinMaxScaler(feature_range=(min, max))
    df = pd.DataFrame(scaler.fit_transform(df), index = df.index, columns=df.columns)

    return df
    
