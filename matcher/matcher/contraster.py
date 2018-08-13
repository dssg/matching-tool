# coding: utf-8

import os

import datetime
import recordlinkage as rl
import pandas as pd

from matcher.logger import logger
import matcher.utils as utils


def truncate_string(s: pd.Series, n: int) -> pd.Series:
    if n > 0:
        s = s.astype(str).apply(lambda x: x[:n])
    elif n < 0:
        s = s.astype(str).apply(lambda x: x[n:])
    else:
        raise ValueError('I cannot compare strings of 0 length!!!')
    return s


def compare_exact_n_chars(s1: pd.Series, s2: pd.Series, n: int) -> pd.Series:
    logger.debug(f'Doing an exact comparison of {n} characters')
    s1 = truncate_string(s1, n)
    s2 = truncate_string(s2, n)
    return (s1 == s2).astype(float)


def lists_share_any_values(l1: pd.Series, l2: pd.Series) -> pd.Series:
    df = pd.concat([l1, l2], axis=1, keys=['l1','l2'])
    return df.apply(lambda row: any(i in row.l2 for i in row.l1), axis=1).astype(float)


def lists_share_all_values(l1: pd.Series, l2: pd.Series) -> pd.Series:
    df = pd.concat([l1, l2], axis=1, keys=['l1','l2'])
    l1_all = df.apply(lambda row: all(i in row.l2 for i in row.l1), axis=1)
    l2_all = df.apply(lambda row: all(i in row.l1 for i in row.l2), axis=1)
    return (l1_all & l2_all).astype(float)


class Contraster:
    def __init__(self, config: dict):
        self.contraster = rl.Compare()
        self.config = config
        self.initialized_time = datetime.datetime.now()

    def compare_exact(self, col_name: str, n_chars: int = None):
        logger.debug(f'Doing an exact comparison on {col_name}')
        if n_chars is not None:
            logger.debug(f'Doing an exact comparison of {n_chars} characters of {col_name}')
            self.contraster.compare_vectorized(
                comp_func=compare_exact_n_chars,
                labels_left=col_name,
                labels_right=col_name,
                n=n_chars['n_chars'],
                label=f"{col_name}_exact_{n_chars['n_chars']}_distance"
            )
        else:
            logger.debug(f'Doing an exact comparison of all characters in {col_name}')
            self.contraster.exact(
                left_on=col_name,
                right_on=col_name,
                label=f'{col_name}_exact_distance'
            )
    
    def compare_string_distance(self, col_name: str, args: dict):
        logger.debug(f'Doing a comparison of {col_name} using {args}')
        self.contraster.string(
            left_on=col_name,
            right_on=col_name,
            label=f'{col_name}_{utils.convert_dict_to_str(args)}_distance',
            **args
        )

    def compare_swap_month_days(self, col_name: str, args: dict):
        logger.debug(f'Checking if the month and day are swapped in {col_name}')
        self.contraster.date(
            left_on=col_name,
            right_on=col_name,
            label=f'{col_name}_swap_month_days_distance',
            **args
        )

    def compare_numeric_distance(self, col_name: str, args: dict):
        logger.debug(f'Doing a numeric distance calculation on {col_name}')
        self.contraster.numeric(
            left_on=col_name,
            right_on=col_name,
            label=f'{col_name}_numeric_{utils.convert_dict_to_str(args)}_distance',
            **args
        )

    def compare_list(self, col_name: str, args: dict):
        if args['method'] == 'any':
            logger.debug(f'Checking if {col_name} shares any value.')
            self.contraster.compare_vectorized(
                comp_func=lists_share_any_values,
                labels_left=col_name,
                labels_right=col_name,
                label=f'{col_name}_any_list_item_distance'
            )

        elif args['method'] == 'all':
            logger.debug(f'Checking if {col_name} shares all values.')
            self.contraster.compare_vectorized(
                comp_func=lists_share_all_values,
                labels_left=col_name,
                labels_right=col_name,
                label=f'{col_name}_all_list_items_distance'
            )

        else:
            raise ValueError(f"I don't know how to compare lists with method {method}. Please send me 'all' or 'any'.")

    def describe_contrasts(self, contrasts):
        contrast_descriptives = {}
        for column in contrasts.columns:
            logger.debug(f'Making you some stats about {column}')
            contrast_descriptives[column] = utils.summarize_column(contrasts[column])
        self.contrast_descriptives = contrast_descriptives

    def run(self, pairs: pd.MultiIndex, df: pd.DataFrame) -> pd.DataFrame:
        """ Read the config and make the required contrasts.

            The config dictionary keys are column names. The values define
            the contrasts to make for the given column. Each definition is a
            dictionary with with a `method` key and (optionally) an `args`
            key containing a dictionary of arguments to pass to the method.

            We will loop over the column names and the contrast definitions and
            call the appropriate method for each.
        """
        self.run_start_time = datetime.datetime.now()
        logger.debug(f'Making the following contrasts: \n{self.config}')
        
        for col_name, contrast_definitions in self.config.items():
            logger.debug(f'Found the following contrasts for {col_name}: \n{contrast_definitions}')

            for contrast_definition in contrast_definitions:
                logger.debug(f"Trying out {contrast_definition['method']} on {col_name}.")
                contrast_method = getattr(self, contrast_definition['method'])

                if 'args' in contrast_definition.keys():
                    logger.debug(f"Passing {contrast_definition['args']} to {contrast_definition['method']}")
                    contrast_method(col_name, contrast_definition['args'])
 
                else:
                    logger.debug(f"Found no arguments for {col_name} {contrast_definition['method']}.")
                    contrast_method(col_name)
        
        logger.debug('Running all those contrasts!')
        contrasts = self.contraster.compute(pairs, df)
        
        self.describe_contrasts(contrasts)

        self.contrast_dataframe_dimensions = contrasts.shape
        self.run_end_time = datetime.datetime.now()
        
        return contrasts

