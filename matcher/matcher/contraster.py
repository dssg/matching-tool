# coding: utf-8

import os

import recordlinkage as rl
import pandas as pd
import yaml

from matcher.logger import logger


# load environment variables
CONTRASTER_CONFIG_FILE = os.getenv('CONTRAST_RULES_CONFIG_NAME')


def truncate_string(s:pd.Series, n:int) -> pd.Series:
    if n > 0:
        s = s.astype(str).apply(lambda x: x[:n])
    elif n < 0:
        s = s.astype(str).apply(lambda x: x[n:])
    else:
        raise ValueError('I cannot compare strings of 0 length!!!')
    return s


def compare_exact_n_chars(s1:pd.Series, s2:pd.Series, n:int) -> pd.Series:
    logger.debug(f'Doing an exact comparison of {n} characters')
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

def args_to_str(args:dict):
    s = str(args)
    s = s.replace("{", "")
    s = s.replace("}", "")
    s = s.replace(" ", "")
    s = s.replace(":", "")
    s = s.replace("'", "")
    return s


class Contraster:
    def __init__(self):
        self.contraster = rl.Compare()

    def compare_exact(self, col_name:str, n_chars=None):
        logger.debug(f'Doing an exact comparison on {col_name}')
        if n_chars is not None:
            logger.debug(f'Doing an exact comparison of {n_chars} characters of {col_name}')
            self.contraster.compare_vectorized(compare_exact_n_chars, col_name, col_name, n_chars['n_chars'], label=f"{col_name}_exact_{n_chars['n_chars']}_distance")
        else:
            logger.debug(f'Doing an exact comparison of all characters in {col_name}')
            self.contraster.exact(col_name, col_name, label=f'{col_name}_exact_distance')
    
    def compare_string_distance(self, col_name:str, args):
        logger.debug(f'Doing a comparison of {col_name} using {args}')
        self.contraster.string(col_name, col_name, label=f'{col_name}_{args_to_str(args)}_distance', **args)

    def compare_swap_month_days(self, col_name:str, args):
        logger.debug(f'Checking if the month and day are swapped in {col_name}')
        self.contraster.date(col_name, col_name, label=f'{col_name}_swap_month_days_distance', **args)

    def compare_numeric_distance(self, col_name:str, args):
        logger.debug(f'Doing a numeric distance calculation on {col_name}')
        self.contraster.date(col_name, col_name, label=f'{col_name}_numeric_{args_to_str(args)}_distance', **args)

    def compare_list(self, col_name:str, args):
        if args['method'] == 'any':
            logger.debug(f'Checking if {col_name} shares any value.')
            self.contraster.compare_vectorized(lists_share_any_values, col_name, col_name, label=f'{col_name}_any_list_item_distance')
        elif args['method'] == 'all':
            logger.debug(f'Checking if {col_name} shares all values.')
            self.contraster.compare_vectorized(lists_share_all_values, col_name, col_name, label=f'{col_name}_all_list_items_distance')
        else:
            raise ValueError(f"I don't know how to compare lists with this method ({method}). Please send me 'all' or 'any'.")


def generate_contrasts(pairs:pd.MultiIndex, df:pd.DataFrame) -> pd.DataFrame:
    logger.debug(f'Reading contrast rules from {CONTRASTER_CONFIG_FILE}')
    with open(CONTRASTER_CONFIG_FILE) as f:
        all_contrasts = yaml.load(f)
    logger.debug(f'Read the following rules: \n{all_contrasts}')
    c = Contraster() 
    for col_name, contrasts in all_contrasts.items():
        logger.debug(f'Found the following contrasts for {col_name}: \n{contrasts}')
        for contrast in contrasts:
            logger.debug(f"Trying out {contrast['method']} on {col_name}.")
            method_to_call = getattr(c, contrast['method'])
            if 'args' in contrast.keys():
                logger.debug(f"Passing {contrast['args']} to {contrast['method']}")
                method_to_call(col_name, contrast['args'])
            else:
                logger.debug(f"Found no arguments for {col_name} {contrast['method']}.")
                method_to_call(col_name)
    logger.debug('Running all those contrasts!')
    return c.contraster.compute(pairs, df)

