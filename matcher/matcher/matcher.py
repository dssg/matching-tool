# coding: utf-8

import pandas as pd

from typing import List

import matcher.featurizer as featurizer
import matcher.rules as rules
import matcher.cluster as cluster
import matcher.ioutils as ioutils

from matcher.logger import logger

import recordlinkage as rl

def run(df:pd.DataFrame, clustering_params:dict, jurisdiction:str, upload_id:str) -> pd.DataFrame:

    ## We will split-apply-combine

    grouped = df.groupby('first_name')

    matches = {}
    logger.debug(f"{df.first_name.value_counts()}")

    for key, group in grouped:
        logger.debug(f"Processing group: {key}")
        logger.debug(f"Group size: {len(group)}")

        if len(group) > 1:

            indexer = rl.FullIndex()
            pairs = indexer.index(group)

            logger.debug(f"Number of pairs: {len(pairs)}")

            logger.debug(f"Initializing featurization")
            features = featurizer.generate_features(pairs, df)
            logger.debug(f"Features created")

            features.index.rename(['matcher_index_left', 'matcher_index_right'], inplace=True)
            features = rules.compactify(features, operation='mean')
            ioutils.write_dataframe_to_s3(features.reset_index(), key=f'csh/matcher/{jurisdiction}/match_cache/features/{upload_id}/{key}')

            logger.debug(f"Features dataframe size: {features.shape}")
            logger.debug(f"Features data without duplicated indexes: {features[~features.index.duplicated(keep='first')].shape}")
            logger.debug("Duplicated keys:")
            logger.debug(f"{features[features.index.duplicated(keep=False)]}")

            matched = cluster.generate_matched_ids(
                distances=features,
                DF=group,
                clustering_params=clustering_params,
                jurisdiction=jurisdiction, # at some point, we may want to consider making the matcher into a class
                upload_id=upload_id,       # rather than passing around keys, upload_ids, jurisdictions, etc.
                block_name=key
            )

            matches[key] = matched
        else:
            logger.debug(f"Group {key} only have one record, making a singleton id")
            matches[key] = cluster.generate_singleton_id(group, key)

    return matches
