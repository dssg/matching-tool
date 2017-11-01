# coding: utf-8

import logging
logger = logging.getLogger('indexer')

import pandas as pd


def identity(df):
    ## Every row in the data frame belongs to the same index, i.e. every row will be compare with every other row
    logger.debug("Creating subsets")
    df.loc[:,('index')] = 1
    logger.debug(f"Subsets created: {df['index'].nunique()}")

    return  df
