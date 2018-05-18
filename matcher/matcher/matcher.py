# coding: utf-8

import pandas as pd
import datetime
import numpy as np

from typing import List

import matcher.contraster as contraster
import matcher.rules as rules
import matcher.cluster as cluster
import matcher.ioutils as ioutils
import matcher.utils as utils

from matcher.logger import logger

import recordlinkage as rl


class Matcher:
    def __init__(self, jurisdiction:str, match_job_id:str, clustering_rules:dict, contrast_rules, blocking_rules:dict=None):
        self.clustering_rules = clustering_rules
        self.jurisdiction = jurisdiction
        self.match_job_id = match_job_id
        self.contrast_rules = contrast_rules
        self.blocking_rules = blocking_rules
        self.metadata = {'matcher_initialization_time': datetime.datetime.now()}

    def block_and_match(self, df):
        ## We will split-apply-combinei
        logger.debug(f'df sent to block-and-match has the following columns: {df.dtypes}')
        logger.info(f'Blocking by {self.blocking_rules}')
        grouped = df.groupby([utils.unpack_blocking_rule(df, column_name, position) for column_name, position in self.blocking_rules.items()])
        logger.info(f'Applying matcher to {len(grouped)} blocks.')
        all_block_metadata = {}

        matches = {}

        for key, group in grouped:
            logger.debug(f"Matching group {key} of size {len(group)}")
            
            if len(group) > 1:
                matches[key], block_metadata = self.match(group, key)
            else:
                block_metadata = {
                    'size': 1,
                    'n_pairs': 0,
                    'features': None,
                    'scores': None
                }
                logger.debug(f"Group {key} only has one record, making a singleton id")
                matches[key] = cluster.generate_singleton_id(group, str(key))

            logger.debug('Wrapping up block')
            all_block_metadata[key] = block_metadata

        logger.debug('All blocks done! Yehaw!')
        self.metadata['blocks'] = all_block_metadata
        return matches

    def match(self, df:pd.DataFrame, key='all') -> pd.DataFrame:
        
        metadata = {
            'size': len(df)
        }
        logger.debug('Indexing the data for matching!')
        indexer = rl.FullIndex()
        pairs = indexer.index(df)
        metadata['n_pairs'] = len(pairs)
        logger.debug(f"Number of pairs: {metadata['n_pairs']}")

        logger.debug(f"Initializing contrasting")
        contraster_obj = contraster.Contraster(self.contrast_rules)
        contrasts = contraster_obj.run(pairs, df)
        metadata['contraster_metadata'] = contrast_object.metadata
        logger.debug(f"Contrasts created")

        contrasts.index.rename(['matcher_index_left', 'matcher_index_right'], inplace=True)
        contrasts = rules.compactify(features, operation='mean')
        logger.debug('Summary distances generated. Making you some stats about them.')
        metadata['scores'] = utils.summarize_column(contrasts.matches)
        logger.debug('Caching those features and distances for you.')
        ioutils.write_dataframe_to_s3(features.reset_index(), key=f'csh/matcher/{self.jurisdiction}/match_cache/features/{self.match_job_id}/{key}')

        logger.debug(f"Features dataframe size: {features.shape}")
        logger.debug(f"Features data without duplicated indexes: {features[~features.index.duplicated(keep='first')].shape}")
        logger.debug("Duplicated keys:")
        logger.debug(f"{features[features.index.duplicated(keep=False)]}")

        matches = cluster.generate_matched_ids(
            distances=features,
            DF=df,
            clustering_params=self.clustering_params,
            jurisdiction=self.jurisdiction, # at some point, we may want to consider making the matcher into a class
            match_job_id=self.match_job_id,       # rather than passing around keys, match_job_ids, jurisdictions, etc.
            block_name=str(key)
        )

        return matches, metadata

