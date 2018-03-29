# coding: utf-8

import pandas as pd

from typing import List

from . import featurizer
from . import rules
from . import cluster
from . import utils

from . import api

import recordlinkage as rl

from flask import current_app

def run(df:pd.DataFrame, clustering_params:dict) -> pd.DataFrame:


    ## We will split-apply-combine

    grouped = df.groupby('first_name')

    matches = {}

    current_app.logger.debug(f"{df.first_name.value_counts()}")
    
    for key, group in grouped:
        current_app.logger.debug(f"Processing group: {key}")
        current_app.logger.debug(f"Group size: {len(group)}")

        if len(group) > 1:
        
            indexer = rl.FullIndex()
            pairs = indexer.index(group)

            current_app.logger.debug(f"Number of pairs: {len(pairs)}")

            current_app.logger.debug(f"Initializing featurization")
            features = featurizer.generate_features(pairs, df)
            current_app.logger.debug(f"Features created")
        
            features.index.rename(['a', 'b'], inplace=True)
            utils.write_to_s3(features.reset_index(), f"csh/matcher/features/{key}")
            features = rules.compactify(rules.scale(features), operation='mean')
            utils.write_to_s3(features.reset_index(), f"csh/matcher/features_scaled/{key}")

            current_app.logger.debug(f"Features dataframe size: {features.shape}")

            current_app.logger.debug(f"Features data without duplicated indexes: {features[~features.index.duplicated(keep='first')].shape}")

            current_app.logger.debug("Duplicated keys:") 
            current_app.logger.debug(f"{features[features.index.duplicated(keep=False)]}")

            f = features.reset_index()
            
            current_app.logger.debug(f"{f[f.a == f.b]}")

            current_app.logger.debug(f"{features[~features.index.duplicated(keep='first')].matches.unstack(level=0, fill_value=1)}")

            matched = cluster.generate_matched_ids(
                distances = features[~features.index.duplicated(keep='first')].matches.unstack(level=-1, fill_value=1),
                DF = group,
                clustering_params=clustering_params
            )

            matches[key] = matched
        else:
            current_app.logger.debug(f"Group {key} only have one record, Ignoring")

    return matches

