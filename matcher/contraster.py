# coding: utf-8

"""
Module for encapsulating the matching process
"""

import numpy as np
import pandas as pd
import itertools

import utils
import distances
import rules

def exact(df, keys):
    """
    Applies the *exact* rule. The distance used is an exact match too.
    """
    return rules.exact(
        distances.exact(
            utils.cartesian(df),
            keys
        )
    )
    


