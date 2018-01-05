# coding: utf-8

__version__='0.0.1'

import logging
logger = logging.getLogger('matcher')

import pandas as pd

from typing import List, Callable
from sklearn.cluster import DBSCAN

from . import utils ## Any idea about how to improve this?
from . import indexer
from . import contraster


def select_columns(df:pd.DataFrame, keys:list) -> pd.DataFrame:
    """ 
    Reduces the dataframe to the columns selected for matching.
    
    We always expect at least two columns: source and source_id
    """
    
    columns_to_select = ['source', 'source_id']
    if keys:
        columns_to_select = columns_to_select + keys
    
    return df.loc[:,columns_to_select]


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


def match(df:pd.DataFrame, contraster:Callable[[pd.DataFrame], pd.DataFrame], keys: List) -> pd.DataFrame:
    """
    """
    logger.info(f"Starting matching process using the strategy {contraster.__name__}")

    df = contraster(df, keys)

    logger.info(f"Matching {contraster.__name__} done")

    return df


def cluster(
    df:pd.DataFrame,
    eps=0.5,
    min_samples=1,
    algorithm='auto',
    leaf_size=30,
    n_jobs=1
) -> pd.DataFrame:
    logging.warning(eps)
    logging.warning(type(eps))
    logging.info('Beginning clustering.')
    df = 1 - df
    clusterer = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric='precomputed',
        metric_params=None,
        algorithm=algorithm,
        leaf_size=leaf_size,
        p=None,
        n_jobs=n_jobs
    )
    clusterer.fit(X=df)
    logging.info('Clustering done!')
    return pd.DataFrame({
        'source_id': clusterer.core_sample_indices_,
        'matched_id': clusterer.labels_
    })


def run(
    df:pd.DataFrame,
    keys:List,
    indexer:Callable[[pd.DataFrame],
    pd.DataFrame],
    contraster:Callable[[pd.DataFrame],pd.DataFrame],
    clustering_params:dict
) -> pd.DataFrame:
    df =  utils.version(
        match(
            df=indexing(
                select_columns(df, keys),
                indexer=indexer
            ),
            contraster=contraster,
            keys=keys
        )
    )

    ids = cluster(
        df.pivot(index='source_id_left', columns='source_id_right', values='matches'),
        **clustering_params
    )

    return (ids)


if __name__ == "main":
    df = None
    
    keys = None
    indexer = indexer.identity
    contraster = contraster.exact
    
    run(df, keys, indexer, contraster)
