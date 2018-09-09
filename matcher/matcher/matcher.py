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
import matcher.ioutils as ioutils
import matcher.utils as utils

from matcher.logger import logger

import recordlinkage as rl


class Matcher:
    def __init__(
        self,
        base_data_directory:str,
        contraster:Contraster,
        scorer:Scorer,
        clusterer:Clusterer
    ):
        self.base_data_directory = base_data_directory
        self.contraster = contraster
        self.scorer = scorer
        self.clusterer = clusterer
        self.initialization_time = datetime.datetime.now()
        self.run_start_time = None
        self.run_end_time = None
        
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
            logger.debug("Contrasts created!")

            logger.debug('Scoring the distances between records.')
            contrasts.index.rename(['matcher_index_left', 'matcher_index_right'], inplace=True)
            contrasts = self.scorer.run(contrasts)
            logger.debug('Caching those contrasts and distances for you.')
            # ioutils.write_dataframe(
            #     contrasts.reset_index(),
            #     filepath=f'{self.base_data_directory}/match_cache/contrasts/{self.match_job_id}/{key}'
            # )
            logger.debug('Scores created.')

            logger.debug('Clustering records!')
            matches = self.clusterer.run(distances=contrasts)
            logger.debug('Clustering done. Wrapping up matching.')

        self.run_end_time = datetime.datetime.now()

        return matches
