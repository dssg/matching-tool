# coding: utf-8

import pandas as pd
import numpy as np

def exact(df:pd.DataFrame) -> pd.DataFrame:
    """
    Checks if the two rows are an exact match. The result will be stored in the column "matches"
    """

    df["matches"] = df.loc[:, df.columns.str.startswith("exact_distance_in")].apply(lambda row: np.all(row), axis=1)

    return df


def compactify(df:pd.DataFrame, operation='sum') -> pd.DataFrame:

    if operation == 'sum':
        df["matches"] = df.filter(like='distance').apply(lambda row: np.sum(row), axis=1)
    elif operation == 'norm':
        df["matches"] = df.filter(like='distance').apply(lambda row: np.linalg.norm(row), axis=1)
    else:
        print(f"Operation {operation} not supported")
        df["matches"] = np.nan
    
    return df
             
