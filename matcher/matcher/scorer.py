# coding: utf-8

import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

class Scorer():
    def __init__(self, operation="sum", reverse=True):
        self.operation = operation
        self.reverse = reverse

    def compactify(contrasted_df:pd.DataFrame) -> pd.DataFrame:
        scored_df = contrasted_df.copy()
        
        if self.operation == 'sum':
            scored_df["matches"] = scored_df.apply(lambda row: np.sum(row), axis=1)
        elif self.operation == 'norm':
            scored_df["matches"] = scored_df.apply(lambda row: np.linalg.norm(row), axis=1)
        elif self.operation == 'mean':
            scored_df['matches'] = scored_df.apply(lambda row: np.mean(row), axis=1)
        else:
            print(f"Operation {operation} not supported")
            scored_df["matches"] = np.nan
        
        if self.reverse:
            scored_df['matches'] = 1 - scored_df['matches']

        return scored_df
    

