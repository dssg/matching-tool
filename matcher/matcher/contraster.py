# coding: utf-8

"""
Module for encapsulating the matching process
"""

import numpy as np
import pandas as pd
import itertools

from . import utils
from . import distances
from . import rules

from typing import List, Callable, Dict

def exact(df:pd.DataFrame, keys:List) -> pd.DataFrame:
    """
    Applies the *exact* rule. The distance used is an exact match too.
    """
    return rules.exact(
        distances.exact(
            utils.cartesian(df, df),
            keys
        )
    )
    


def generic(df:pd.DataFrame, rule:Callable[[pd.DataFrame, str],pd.DataFrame], dist:Dict) -> pd.DataFrame:
    """
    Applies distances calculations in sequence, and then applies the provided rule
    """

    df = utils.cartesian(df, df)
    
    for distance, keys in dist.items():
        distance_func = getattr(distances, distance)
        distance_func(df, keys)

    return rule(df)

    
