# coding: utf-8

import logging
logger = logging.getLogger('matcher')

import pandas as pd

from typing import List

from . import featurizer
from . import rules
from . import cluster

import recordlinkage as rl


def run(df:pd.DataFrame, clustering_params:dict) -> pd.DataFrame:

    indexer = rl.RandomIndex(n=250_000)   ## TODO: Choose a better n
    pairs = indexer.index(df)
    
    features = featurizer.generate_features(pairs, df)

    features = rules.compactify(rules.scale(features), operation='mean')

    matches = cluster.generate_matched_ids(
        distances = features[features.index.duplicated(keep='first')].matches.unstack(level=1, fill_value=1),
        df = df,
        clustering_params=clustering_params
    )

    return matches

