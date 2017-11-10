# coding: utf-8


import pandas as pd
import numpy as np

from typing import List

def exact(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    """
    Calculates the "exact distance" between all the selected columns
    """

    for col in keys:
        df[f"distance_in_{col}"] = df.loc[:, df.columns.str.startswith(col)].apply(lambda row: row[0] == row[1], axis = 1)
     
    return df


