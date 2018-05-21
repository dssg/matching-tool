# coding: utf-8

import os

import pandas as pd
import smart_open
import botocore
import datetime
import yaml

from matcher.logger import logger
import matcher.utils as utils

# load dotenv
from dotenv import load_dotenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

class Store:
    def __init__(self, base_data_directory:str, match_job_id:str, person_keys:list, schema_pk_lookup:dict):
        self.base_data_directory = base_data_directory
        self.match_job_id = match_job_id
        self.person_keys = person_keys
        self.schema_pk_lookup = schema_pk_lookup
        self.event_types = list(schema_pk_lookup.keys())
        self.event_types_read = []
        self.metadata = {}

    def load_data_for_matching(self):
        logger.debug(f'Loading data for event types: {self.event_types}')
        try:
            df = pd.concat([load_one_event_type(base_data_directory, event_type, keys, match_job_id) for event_type in self.event_types])
        except ValueError as e:
            if str(e) != "All objects passed were None":
                raise
            else:
                logger.debug('Found no data for the event_types given in the base data directory.')
                raise ValueError(f'No merged data files found for any event type ({event_types}) in {base_data_directory}. If you are using S3, make sure your keys are present in the environment.')
        
        df['match_job_id'] = self.match_job_id
        logger.debug(f'Number of deduped events: {len(df)}')

        # Which event types did we read successfully?
        self.event_types_read = df.event_type.drop_duplicates().values
        
        # Drop duplicates, disregarding event type
        self.metadata['number_of_events_read'] = len(df)
        df = df.drop('event_type', axis=1)
        df = df.drop_duplicates(subset=self.person_keys)
        self.metadata['number_of_deduplicated_events_read'] = len(df)

        # Some additional metadata
        self.metadata
