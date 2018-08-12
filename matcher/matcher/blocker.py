# coding: utf-8

import datetime
import pandas as pd

from matcher.logger import logger


class Blocker():

    def __init__(self, blocking_rules:dict):
        self.blocking_rules = blocking_rules
        self.metadata = {'blocker_initialization_time': datetime.datetime.now()}

    def run(self, preprocessed_df:pd.DataFrame) -> pd.core.groupby.DataFrameGroupBy:
        """ Take the preprocessed dataframe, and return a group dictionary of
            dataframes where the keys are the blocking values and the values
            are dataframes containing only records matching the key.
        """
        self.metadata['blocker_run_time'] = datetime.datetime.now()
        logger.info(f"Blocking by {self.blocking_rules}")

        grouped_df = preprocessed_df.groupby([
            self._unpack_blocking_rule(preprocessed_df, column_name, position)
            for column_name, position
            in self.blocking_rules.items()
        ])

        logger.info(f"Blocking is done: got {len(grouped_df)} blocks.")
        self.metadata['num_blocks'] = len(grouped_df)
        self.metadata['block_keys'] = grouped_df.keys

        self.metadata['blocker_finished_time'] = datetime.datetime.now()

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

