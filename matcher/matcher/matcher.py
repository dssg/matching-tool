# coding: utf-8

import logging
logger = logging.getLogger('matcher')

import pandas as pd

from typing import List

import recordlinkage as rl

def run(df:pd.DataFrame, keys:List) -> pd.DataFrame:

    indexer = rl.RandomIndex(n=100_000)   ## TODO: Choose a better n
    pairs = indexer.index(df)
    
    c = rl.Compare()

    for key in keys:   # TODO: Hardcode the comparison. You can remove the for loop
        c.string(key, key, method='jarowinkler', threshold=0.85, label=f"jw_{key}")

    distances = c.compute(pairs, df)

    matches = distances  # Just for testing, (see next TODO)

    # TODO: Choose one from the following

    # threshold = 0       <-- Change this!!
    # matches = distances[distances.sum(axis=1) > threshold]
    
    #kmeans = rl.KMeansClassifier()
    #matches = kmeans.learn(distances, return_type='series')

    #ecm = rl.ECMClassifier()
    #matches = ecm.learn((distances > 0.8).astype(int))

    return matches

