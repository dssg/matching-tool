# coding: utf-8

import pandas as pd
import datetime
import hashlib
import json
import numpy as np
import sklearn

from typing import List

from matcher.contraster import Contraster
from matcher.scorer import Scorer
from matcher.cluster import Clusterer
import matcher.utils as utils

from matcher.logger import logger

import recordlinkage as rl


class Matcher:
    def __init__(
        self,
        contraster:Contraster,
        scorer:Scorer,
        clusterer:Clusterer
    ):
        self.contraster = contraster
        self.scorer = scorer
        self.clusterer = clusterer
        self.initialization_time = datetime.datetime.now()
        self.run_start_time = None
        self.run_end_time = None
        self.contrasts = None

    @property
    def square_distance_matrix(self):
        return self.clusterer.square_distance_matrix

    @property
    def raw_cluster_ids(self):
        return self.clusterer.square_distance_matrix

    def run(self, df:pd.DataFrame) -> pd.DataFrame:
        self.run_start_time = datetime.datetime.now()
        
        # If there's only 1 record, nothing to link; make a matched_id and exit
        if len(df) == 1:
            logger.debug(f"Dataframe only has one record, making a singleton id")
            matches = pd.Series(data=[1], index=df.index)

        # If there's more than one record, start linking records
        else:
            logger.debug('Indexing the data for matching!')
            indexer = rl.FullIndex()
            pairs = indexer.index(df)
            self.n_pairs = len(pairs)
            logger.debug(f"Indexing done. Number of pairs: {self.n_pairs}")

            logger.debug(f"Initializing contrasting!")
            contrasts = self.contraster.run(pairs, df)
            contrasts.index.rename(
                ['matcher_index_left', 'matcher_index_right'], inplace=True
            )
            logger.debug(contrasts)
            logger.debug("Contrasts created!")

            logger.debug('Scoring the distances between records.')
            contrasts = self.scorer.run(contrasts)
            self.contrasts = contrasts.copy()
            logger.debug('Caching those contrasts and distances for you.')
            logger.debug('Scores created.')

            logger.debug('Clustering records!')
            matches = self.clusterer.run(distances=self.contrasts)
            logger.debug('Clustering done. Wrapping up matching.')

        self.run_end_time = datetime.datetime.now()

        return matches

