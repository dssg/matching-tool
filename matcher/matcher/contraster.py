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

from typing import List, Callable

def exact(df1:pd.DataFrame, df2:pd.DataFrame, keys:List) -> pd.DataFrame:
    """
    Applies the *exact* rule. The distance used is an exact match too.
    """
    return rules.exact(
        distances.exact(
            utils.cartesian(df1, df2),
            keys
        )
    )
    


