# coding: utf-8

import pandas as pd
import numpy as np

def exact(df:pd.DataFrame) -> pd.DataFrame:
    """
    Checks if the two rows are an exact match. The result will be stored in the column "matches"
    """

    df["matches"] = df.loc[:, df.columns.str.startswith("distance_in")].apply(lambda row: np.all(row), axis=1)

    return df


