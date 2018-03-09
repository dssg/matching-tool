# coding: utf-8

__version__='0.0.1'

import logging
logger = logging.getLogger('matcher')

import pandas as pd
import numpy as np

from typing import List, Callable

from . import utils
from . import indexer
from . import contraster
from . import transformer
from . import cluster


def indexing(df:pd.DataFrame, indexer:Callable[[pd.DataFrame], pd.DataFrame]) -> pd.DataFrame:
    """
    Creates a subsets of the data frame using a function. This subset will be 
    formed by the *candidate record pairs*

    `func` is an indexing technique as: *blocking*, *sorted neighbourhood indexing* and *q-grams* or simply *identity*

    See for reference:
      - *Probabilistic record linkage with the Fellegi and Sunter framework*, M.S. Thesis, **Jonathan de Bruin** (2015)
    """
    logger.info(f"Starting indexing using the strategy {indexer.__name__}")

    df = indexer(df)

    logger.info(f"Indexing {indexer.__name__} done")

    return df


def match(df:pd.DataFrame, contraster:Callable[[pd.DataFrame], pd.DataFrame], **kwargs) -> pd.DataFrame:
    """
    """
    logger.info(f"Starting matching process using the strategy {contraster.__name__}")

    df = contraster(df, keys)

    logger.info(f"Matching {contraster.__name__} done")

    return df


def run(
    df:pd.DataFrame,
    keys:List,
    indexer:Callable[[pd.DataFrame],
    pd.DataFrame],
    contraster:Callable[[pd.DataFrame],pd.DataFrame],
    clustering_params:dict,
    # df2:pd.DataFrame=None
) -> pd.DataFrame:
    
    df1 = utils.generate_row_ids(df1)
    df1['source_id'] = utils.get_source_id(df1)
    
    # if df2 is None:
    #     df2 = df1.copy()
    #     self_match = True
    # else:
    #     df2 = utils.generate_row_ids(df2)
    #     df2['source_id'] = utils.get_source_id(df2)
    #     self_match = False

    distances =  utils.version(
        match(
            df=indexing(indexer=indexer),
            # df2=indexing(
            #     select_columns(df2, keys),
            #     indexer=indexer
            # ),
            contraster=contraster,
            keys=keys
        )
    )

    df = cluster.generate_matched_ids(
        distances=distances.pivot(index='row_id_left', columns='row_id_right', values='matches'),
        df=df,
        # df2=df2,
        clustering_params=clustering_params
    )

    return (df.drop('row_id', axis=1))


if __name__ == "main":
    df = None
    
    keys = None
    indexer = indexer.identity
    contraster = contraster.exact

    to_ngrams = []
    to_unite = {}
    to_split = []
    
    run(df, keys, indexer, contraster)
