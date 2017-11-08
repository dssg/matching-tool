# coding: utf-8

import numpy as np
import pandas as pd
import itertools

import utils
import distances
import rules

def exact(df, keys):
    return rules.exact(
        distances.exact(
            utils.cartesian(df),
            keys
        )
    )
    


