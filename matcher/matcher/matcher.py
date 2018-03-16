# coding: utf-8

import logging
logger = logging.getLogger('matcher')

import pandas as pd
import numpy as np

from typing import List, Callable

import recordlinkage as rl

def run(df:pd.DataFrame, keys:List) -> pd.DataFrame:
    
    indexer = rl.BlockIndex(on='first_name')
    pairs = indexer.index(df)

    print(len(pairs))
    c = rl.Compare()

    for key in keys:
        c.string(key, key, method='jarowinkler', threshold=0.85, label=f"jw_{key}")

    distances = c.compute(pairs, df)

    
    #kmeans = rl.KMeansClassifier()
    #results = kmeans.learn(distances, return_type='series')

    #ecm = rl.ECMClassifier()
    #result = ecm.learn((distances > 0.8).astype(int))

    #return results 
    return distances

