# coding: utf-8

import recordlinkage as rl
import pandas as pd

from matcher.logger import logger


def truncate_string(s:pd.Series, n:int) -> pd.Series:
    if n > 0:
        s = s.astype(str).apply(lambda x: x[:n])
    elif n < 0:
        s = s.astype(str).apply(lambda x: x[n:])
    else:
        raise ValueError('I cannot compare strings of 0 length!!!')
    return s


def compare_exact_n_chars(s1:pd.Series, s2:pd.Series, n:int) -> pd.Series:
    s1 = truncate_string(s1, n)
    s2 = truncate_string(s2, n)
    return (s1 == s2).astype(float)


def lists_share_any_values(l1:pd.Series, l2:pd.Series) -> pd.Series:
    df = pd.concat([l1, l2], axis=1, keys=['l1','l2'])
    return df.apply(lambda row: any(i in row.l2 for i in row.l1), axis=1).astype(float)


def lists_share_all_values(l1:pd.Series, l2:pd.Series) -> pd.Series:
    df = pd.concat([l1, l2], axis=1, keys=['l1','l2'])
    l1_all = df.apply(lambda row: all(i in row.l2 for i in row.l1), axis=1)
    l2_all = df.apply(lambda row: all(i in row.l1 for i in row.l2), axis=1)
    return (l1_all & l2_all).astype(float)


class Comparer(Object):
    def __init__(self):
        self.comparer = rl.Compare()

    def compare_exact(self, col_name:str, n_chars:int=None):
        if n_chars:
            logger.debug(f'Doing an exact comparison of {n_chars} characters of {col_name}')
            self.comparer.exact(col_name, col_name, label=f'{col_name}_exact_distance')
        else:
            logger.debug(f'Doing an exact comparison of {col_name}')
            self.comparer.compare_vectorized(compare_exact_n_chars, col_name, col_name, n, label=f'{col_name}_exact_{n_chars}_distance')
    
    def compare_string_distance(self, col_name:str, method:str):
        logger.debug(f'Doing a {method} comparison of {col_name}')
        self.comparer.string(col_name, col_name, method=method, label=f'{col_name}_{method}_distance')

    def compare_swap_month_days(self, col_name:str, swap_score:float=None):
        logger.debug(f'Checking if the month and day are swapped in {col_name}')
        self.comparer.date(col_name, col_name, swap_month_day=swap_score, swap_months=None)

    def compare_numeric_distance(self, col_name:str, **kwargs):
        logger.debug(f'Doing a numeric distance calculation on {col_name}')
        self.comparer.date(col_name, col_name, kwargs)

    def compare_list(self, col_name:str, method:str)
        if method == 'any':
            logger.debug(f'Checking if {col_name} shares any value.')
            self.comparer.compare_vectorized(lists_share_any_values, col_name, col_name, label=f'{col_name}_any_list_item_distance')
        elif method == 'all':
            logger.debug(f'Checking if {col_name} shares all values.')
            self.comparer.compare_vectorized(lists_share_all_values, col_name, col_name, label=f'{col_name}_all_list_items_distance')
        else:
            raise ValueError(f"I don't know how to compare lists with this method ({method}). Please send me 'all' or 'any'.")


def generate_features(all_comparisons:dict, pairs:pd.MultiIndex, df:pd.DataFrame) -> pd.DataFrame:
    c = Comparer() 
    for col_name, comparisons in self.all_comparisons:
        for comparison, args in comparison:
            method_to_call = getattr(c.comparer, comparison)
            method_to_call(col_name, args)

    return c.comparer.compute(pairs, df)

