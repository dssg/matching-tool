# coding: utf-8

import datetime
import pandas as pd

from matcher.logger import logger


class Blocker():

    def __init__(self, blocking_rules:dict=None):
        self.blocking_rules = blocking_rules
        self.initialization_time = datetime.datetime.now()
        self.run_start_time = None
        self.num_blocks = None
        self.block_keys = None
        self.run_end_time = None

    def run(self, preprocessed_df:pd.DataFrame) -> pd.core.groupby.DataFrameGroupBy:
        """ Take the preprocessed dataframe, and return a group dictionary of
            dataframes where the keys are the blocking values and the values
            are dataframes containing only records matching the key.
        """
        self.run_start_time = datetime.datetime.now()

        if self.blocking_rules:
            logger.debug(f"Blocking by {self.blocking_rules}")
            grouped_df = preprocessed_df.groupby([
                self._unpack_blocking_rule(preprocessed_df, column_name, position)
                for column_name, position
                in self.blocking_rules.items()
            ])

        else:
            logger.debug('No blocking rules passed. Matching all record pairs.')
            block = pd.Series(data=['all']*len(preprocessed_df), index=preprocessed_df.index)
            grouped_df = preprocessed_df.groupby(block)

        logger.debug(f"Blocking is done: got {len(grouped_df)} blocks.")
        self.num_blocks = len(grouped_df)
        self.block_keys = pd.DataFrame(grouped_df.keys).drop_duplicates().T
        self.run_end_time = datetime.datetime.now()
        
        return grouped_df

    def _unpack_blocking_rule(
            self,
            df:pd.DataFrame,
            column_name:str,
            position:int
        ) -> pd.Series:
        """ Given a blocking rule and a dataframe, convert the relevant column
            to a string and return the value of the key for each row.
        """
        if position < 0:
            return df[column_name].astype(str).str[position:]
        elif position > 0:
            return df[column_name].astype(str).str[:position]
        else:
            raise ValueError(f"I cannot split a string at this position: {position}")

