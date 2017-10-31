# coding: utf-8


import logging

import pandas as pd

from typing import List


def select_columns(df, columns_to_select: List):
    """ Reduces the dataframe to the columns selected for matching.
    """
    return df[columns_to_select]

def indexing(df):
    pass

def deduplicate(df):
    pass


def run(df, columns_to_select):
    return deduplicate(indexing(select_columns(df, columns_to_select)))


if __name__ == "main":
    df = None
    columns_to_select = None

    
    run(df, columns_to_select)
