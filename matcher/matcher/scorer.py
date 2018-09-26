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
        self.initialized_time = datetime.datetime.now()

    def run(self, contrasted_df: pd.DataFrame) -> pd.DataFrame:
        self.run_start_time = datetime.datetime.now()

        logger.debug(f'Scoring record pairs with operation {self.operation}')

        scored_df = contrasted_df.copy()
        logger.debug('Made a copy of contrasts')
        if self.operation == 'sum':
            scored_df['score'] = scored_df.apply(lambda row: np.sum(row), axis=1)
        elif self.operation == 'norm':
            scored_df['score'] = scored_df.apply(lambda row: np.linalg.norm(row), axis=1)
        elif self.operation == 'mean':
            scored_df['score'] = scored_df.apply(lambda row: np.mean(row), axis=1)
            logger.debug('Made scores')
        else:
            raise ValueError(f'Scoring operation {operation} not supported.')
            scored_df['score'] = np.nan

        if self.reverse:
            scored_df['score'] = 1 - scored_df['score']
            logger.debug('Reversed scores')
        self.scores = scored_df['score']
        self.score_descriptives = utils.summarize_column(scored_df.score)
        self.run_end_time = datetime.datetime.now()

        return scored_df

