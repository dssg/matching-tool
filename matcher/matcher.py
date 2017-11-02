# coding: utf-8


import logging
logger = logging.getLogger('matcher')

import pandas as pd

from typing import List

import indexer


def select_columns(df, columns_to_select: List):
    """ 
    Reduces the dataframe to the columns selected for matching.
    """
    return  df[columns_to_select]

def indexing(df, func):
    """
    Creates a subsets of the data frame using a function. This subset will be 
    formed by the *candidate record pairs*

    `func` is an indexing technique as: *blocking*, *sorted neighbourhood indexing* and *q-grams* or simply *identity*

    See for reference:
      - *Probabilistic record linkage with the Fellegi and Sunter framework*, M.S. Thesis, **Jonathan de Bruin** (2015)
    """
    logger.info(f"Starting indexing using the strategy {func.__name__}")

    df = func(df)

    logger.info(f"Indexing {func.__name__} done")

    return df


def deduplicate(df):
    """
    """
    pass


def run(df, columns_to_select, indexing_strategy):
    return  deduplicate(
        indexing(
            select_columns(df, columns_to_select),
            func=indexing_strategy)
    )


if __name__ == "main":
    df = None
    
    columns_to_select = None
    indexing_strategy = indexer.identity
    
    run(df, columns_to_select, indexing_strategy)
