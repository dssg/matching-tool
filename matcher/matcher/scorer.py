# coding: utf-8

import datetime
import pandas as pd
import numpy as np

import matcher.utils as utils

from matcher.logger import logger


class Scorer():
    def __init__(self, operation='mean', reverse=True):
        self.operation = operation
        self.reverse = reverse
        self.metadata{'scorer_initialization_time': datetime.datetime.now()}

    def run(self, contrasted_df:pd.DataFrame) -> pd.DataFrame:
        self.metadata['scorer_run_time'] = datetime.datetime.now()

        logger.debug(f'Scoring record pairs with operation {self.operation}')

        scored_df = contrasted_df.copy()
        
        if self.operation == 'sum':
            scored_df['score'] = scored_df.apply(lambda row: np.sum(row), axis=1)
        elif self.operation == 'norm':
            scored_df['score'] = scored_df.apply(lambda row: np.linalg.norm(row), axis=1)
        elif self.operation == 'mean':
            scored_df['score'] = scored_df.apply(lambda row: np.mean(row), axis=1)
        else:
            raise ValueError(f'Scoring operation {operation} not supported.')
            scored_df['score'] = np.nan

        if self.reverse:
            scored_df['score'] = 1 - scored_df['score']

        self.metadata['scores'] = utils.summarize_column(scored_df.score)
        self.metadata['scorer_finished_time'] = datetime.datetime.now()

        return scored_df

