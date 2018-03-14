# coding: utf-8

import logging
logger = logging.getLogger('matcher')

import pandas as pd
import numpy as np

from typing import List, Callable

import recordlinkage as rl

def run(df:pd.DataFrame, keys:List) -> pd.DataFrame:
    
    indexer = rl.FullIndex()
    pairs = indexer.index(df)

    c = rl.Compare()

    for key in keys:
        c.string(key, key, method='jarowinkler', threshold=0.85, label=f"jw_{key}")

    distances = c.compute(pairs, df)

    return distances


