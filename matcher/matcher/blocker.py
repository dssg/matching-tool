# coding: utf-8


import pandas as pd


class Blocker():

    def __init__(blocking_rules:dict):
        self.blocking_rules = blocking_rules

    def run(preprocessed_df:pd.DataFrame):
        logger.info(f"Blocking by {self.blocking_rules}")
        grouped_df = df.groupby([
            self._unpack_blocking_rule(preprocessed_df, column_name, position)
            for column_name, position
            in blocking_rules.items()
        ])

        logger.info(f"Blocking is done: got {len(grouped_df)} blocks.")

        return grouped_df


    def _unpack_blocking_rule(df, column_name, position):
        if position < 0:
            return df[column_name].astype(str).str[position:]
        elif position > 0:
            return df[column_name].astype(str).str[:position]
        else:
            raise ValueError(f"I cannot split a string at this position: {position}")
