# coding: utf-8

import pandas as pd

from typing import List

import matcher.featurizer as featurizer
import matcher.rules as rules
import matcher.cluster as cluster
import matcher.ioutils as ioutils

from . import api

import recordlinkage as rl

def run(df:pd.DataFrame, clustering_params:dict) -> pd.DataFrame:


    ## We will split-apply-combine

    grouped = df.groupby('first_name')

    matches = {}
    api.app.logger.debug(f"{df.first_name.value_counts()}")
    
    for key, group in grouped:
        api.app.logger.debug(f"Processing group: {key}")
        api.app.logger.debug(f"Group size: {len(group)}")

        if len(group) > 1:
        
            indexer = rl.FullIndex()
            pairs = indexer.index(group)

            api.app.logger.debug(f"Number of pairs: {len(pairs)}")

            api.app.logger.debug(f"Initializing featurization")
            features = featurizer.generate_features(pairs, df)
            api.app.logger.debug(f"Features created")
 
            features.index.rename(['matcher_index_left', 'matcher_index_right'], inplace=True)
            ioutils.write_dataframe_to_s3(features.reset_index(), f"csh/matcher/features/{key}")
            features = rules.compactify(features, operation='mean')
            ioutils.write_dataframe_to_s3(features.reset_index(), f"csh/matcher/features_scaled/{key}")

            api.app.logger.debug(f"Features dataframe size: {features.shape}")

            api.app.logger.debug(f"Features data without duplicated indexes: {features[~features.index.duplicated(keep='first')].shape}")

            api.app.logger.debug("Duplicated keys:") 
            api.app.logger.debug(f"{features[features.index.duplicated(keep=False)]}")
            f = features.reset_index()

            api.app.logger.debug(f"{f[f.matcher_index_left == f.matcher_index_right]}")

            api.app.logger.debug(f"{features[~features.index.duplicated(keep='first')].matches.unstack(level=0, fill_value=1)}")

            api.app.logger.debug('Generating inverse pairs (flip left/right ordering)')
            f.rename({'matcher_index_left': 'matcher_index_right', 'matcher_index_right': 'matcher_index_left'}, axis='columns', inplace=True)
            f.set_index(['matcher_index_left', 'matcher_index_right'], inplace=True)
            matched = cluster.generate_matched_ids(
                distances = pd.concat([features, f]).matches.unstack(level=-1, fill_value=0),
                DF = group,
                clustering_params=clustering_params,
                block_name=key
            )

            matches[key] = matched
        else:
            api.app.logger.debug(f"Group {key} only have one record, making a singleton id")
            matches[key] = cluster.generate_singleton_id(group, key)

    return matches

