# coding: utf-8

import pandas as pd
import datetime
import numpy as np

from typing import List

import matcher.contraster as contraster
import matcher.scorer as scorer
import matcher.cluster as cluster
import matcher.ioutils as ioutils
import matcher.utils as utils

from matcher.logger import logger

import recordlinkage as rl


class Matcher:
    def __init__(
        self,
        base_data_directory:str,
        match_job_id:str,
        clustering_rules:dict,
        contrast_rules,
        blocking_rules:dict=None
    ):
        self.clustering_rules = clustering_rules
        self.base_data_directory = base_data_directory
        self.match_job_id = match_job_id
        self.contrast_rules = contrast_rules
        self.blocking_rules = blocking_rules
        self.metadata = {'matcher_initialization_time': datetime.datetime.now()}
        self.scorer = scorer.Scorer(operation='mean')

    def run(self, df:pd.DataFrame, key='all') -> pd.DataFrame:
        self.metadata['matcher_run_time'] = datetime.datetime.now()

        # If there's only 1 record, nothing to link; make a matched_id and exit
        if len(group) = 1:
            logger.debug(f"Dataframe only has one record, making a singleton id")
            matches = cluster.generate_singleton_id(df, str(key))
            self.metadata.update({
                'size': 1,
                'n_pairs': 0,
                'contrasts': None,
                'scores': None
            })

        # If there's more than one record, start linking records
        else:
            self.metadata['size'] = len(df)
            logger.debug('Indexing the data for matching!')
            indexer = rl.FullIndex()
            pairs = indexer.index(df)
            self.metadata['n_pairs'] = len(pairs)
            logger.debug(f"Number of pairs: {self.metadata['n_pairs']}")

            logger.debug(f"Initializing contrasting")
            contraster_obj = contraster.Contraster(self.contrast_rules)
            contrasts = contraster_obj.run(pairs, df)
            self.metadata['contraster_metadata'] = contraster_obj.metadata
            logger.debug(f"Contrasts created")

            contrasts.index.rename(['matcher_index_left', 'matcher_index_right'], inplace=True)
            contrasts = self.scorer.run(contrasts)
            logger.debug('Summary distances generated. Making you some stats about them.')
            self.metadata['scores'] = utils.summarize_column(contrasts.matches)
            logger.debug('Caching those contrasts and distances for you.')
            ioutils.write_dataframe(contrasts.reset_index(), filepath=f'{self.base_data_directory}/match_cache/contrasts/{self.match_job_id}/{key}')

            logger.debug(f"Contrasts dataframe size: {contrasts.shape}")
            logger.debug(f"Contrasts data without duplicated indexes: {contrasts[~contrasts.index.duplicated(keep='first')].shape}")
            logger.debug("Duplicated keys:")
            logger.debug(f"{contrasts[contrasts.index.duplicated(keep=False)]}")

            matches = cluster.generate_matched_ids(
                distances=contrasts,
                DF=df,
                clustering_params=self.clustering_rules,
                base_data_directory=self.base_data_directory, # at some point, we may want to consider making the matcher into a class
                match_job_id=self.match_job_id,       # rather than passing around keys, match_job_ids, base_data_directorys, etc.
                block_name=str(key)
            )

        return matches

