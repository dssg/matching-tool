# coding: utf-8

import logging
logger = logging.getLogger('matcher')

import pandas as pd

from typing import List

from . import featurizer
from . import rules
from . import cluster
from . import utils

import recordlinkage as rl


def run(df:pd.DataFrame, clustering_params:dict) -> pd.DataFrame:

    indexer = rl.BlockIndex('first_name')   ## TODO: Choose a better n
    pairs = indexer.index(df)
    
    features = featurizer.generate_features(pairs, df)

    features.index.rename(['a', 'b'], inplace=True)
    utils.write_to_s3(features.reset_index(), 'csh/matcher/features')
    features = rules.compactify(rules.scale(features), operation='mean')
    utils.write_to_s3(features.reset_index(), 'csh/matcher/features_scaled')
    matches = cluster.generate_matched_ids(
        distances = features[features.index.duplicated(keep='first')].matches.unstack(level=1, fill_value=1),
        df = df,
        clustering_params=clustering_params
    )

    return matches

