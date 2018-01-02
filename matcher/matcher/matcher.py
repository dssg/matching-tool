# coding: utf-8

__version__='0.0.1'

import logging
logger = logging.getLogger('matcher')

import pandas as pd

from typing import List, Callable


from . import utils ## Any idea about how to improve this?
from . import indexer
from . import contraster


def select_columns(df:pd.DataFrame, keys: List) -> pd.DataFrame:
    """ 
    Reduces the dataframe to the columns selected for matching.

    We always expect at least two columns: source and source_id
    """

    columns_to_select = ['source', 'source_id']
    if keys:
        columns_to_select = columns_to_select + keys
    
    return  df.loc[:,columns_to_select]

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


def run(df:pd.DataFrame, keys:List, indexer:Callable[[pd.DataFrame], pd.DataFrame], contraster:Callable[[pd.DataFrame], pd.DataFrame]) -> pd.DataFrame:
    return  utils.version(
        match(
            df=indexing(
                select_columns(df, keys),
                indexer=indexer
            ),
            contraster=contraster,
            keys=keys
        )
    )


if __name__ == "main":
    df = None
    
    keys = None
    indexer = indexer.identity
    contraster = contraster.exact
    
    run(df, keys, indexer, contraster)
