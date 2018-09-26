# coding: utf-8

import io
import os
from os.path import dirname

import pandas as pd
import s3fs
import yaml
from urllib.parse import urlparse
from contextlib import contextmanager

from matcher.logger import logger
from matcher import  utils

# load dotenv
from dotenv import load_dotenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


class Store(object):
    def __init__(self, base_data_directory):
        self.base_data_directory = base_data_directory

    def load(self, path:str):
        with self._open(path) as f:
            return f.read()

    def write_dataframe(self, df:pd.DataFrame, path:str) -> None:
        with self._open(path, 'wb') as fout:
            fout.write(df.to_csv(sep='|', index=False).encode())

        logger.info(f'Wrote data to {path}.')

    @contextmanager
    def _open(self, path, *args, **kwargs):
        """Opens files either on s3 or a filesystem according to the path's scheme

        Uses s3fs so boto3 is used.
        This means mock_s3 can be used for tests, instead of the mock_s3_deprecated
        """
        full_path = f'{self.base_data_directory}/{path}'
        logger.debug(f'Opening {full_path}')
        path_parsed = urlparse(full_path)
        scheme = path_parsed.scheme  # If '' or 'file' then a regular file; if 's3' then 's3'

        if not scheme or scheme == 'file':  # Local file
            os.makedirs(dirname(full_path), exist_ok=True)
            with open(full_path, *args, **kwargs) as f:
                yield f
        elif scheme == 's3':
            s3 = s3fs.S3FileSystem()
            with s3.open(full_path, *args, **kwargs) as f:
                yield f


class Cache(object):
    def __init__(
        self,
        store,
        match_job_id:str,
        loaded_data:bool=False,
        preprocessed_data:bool=False,
        contrasts:bool=False,
        square_distances:bool=False,
        raw_cluster_ids:bool=False,
        matcher_results:bool=False
    ):
        self.store = store
        self.match_job_id = match_job_id
        self.loaded_data = loaded_data
        self.preprocessed_data = preprocessed_data
        self.contrasts = contrasts
        self.square_distances = square_distances
        self.raw_cluster_ids = raw_cluster_ids
        self.matcher_results = matcher_results

    def _cache(self, df:pd.DataFrame, path:str) -> None:
        self.store.write_dataframe(df=df, path=f'{path}/{self.match_job_id}')

    def cache_matcher_data(self, df, df_type) -> None:
        if getattr(self, df_type):
            logger.info(f'Caching {df_type}.')
            self._cache(df=df.reset_index(), path=f'match_cache/{df_type}')
        else:
            logger.info(f'Skipping cache of {df_type}; flag not set.')

    def cache_events(self, df, event_type):
        self._cache(df=df, path=f'{event_type}/matches')


class MatcherServiceStore(object):
    def __init__(
        self,
        store,
        cache,
        schema_pk_lookup:dict,
        matching_keys:list
    ):
        self.store = store
        self.cache = cache
        self.schema_pk_lookup = schema_pk_lookup
        self.matching_keys = matching_keys
        self.event_types_read = []

    def load_data_for_matching(self) -> list:
        logger.debug(f'Loading data for event types: {self.schema_pk_lookup.keys()}')
        try:
            df = pd.concat([self._try_loading_event_data(event_type) for event_type in self.schema_pk_lookup.keys()])
        except ValueError as e:
            if str(e) == 'All objects passed were None':
                logger.debug('Found no events data.')
                raise ValueError(f'No merged data found for any event type ({self.schema_pk_lookup.keys()}).')
            else:
                raise
        logger.debug(f'Number of events: {len(df)}')
        
        ## add the match_job_id
        df['match_job_id'] = self.cache.match_job_id

        # Drop duplicates, disregarding event type
        df = df.drop_duplicates(subset=self.matching_keys)

        logger.debug(f'The loaded dataframe has the following columns: {df.columns}')
        logger.debug(f'The dimensions of the loaded and deduped dataframe are: {df.shape}')
        logger.debug(f'The indices of the loaded dataframe are {df.index}')

        # Cache read data
        self.cache.cache_matcher_data(df=df, df_type='loaded_data') 

        return df

    def _try_loading_event_data(self, event_type:str) -> pd.DataFrame:
        logger.info(f'Loading {event_type} data for matching.') 

        try:
            df = self._read_merged_data(event_type)

            # Dropping columns that we don't need for matching
            df = df[self.matching_keys]

            logger.info(f'{len(df)} events loaded for {event_type}.')
            self.event_types_read.append(event_type)

            return df

        except FileNotFoundError as e:
            logger.info(f'No merged file found for {event_type}. Skipping.')
            pass

    def _read_merged_data(self, event_type:str) -> pd.DataFrame:
        merged_filepath = f'{event_type}/merged'
        logger.info(f'Reading data from {merged_filepath}')
        df = pd.read_csv(io.BytesIO(self.store.load(merged_filepath)), sep='|')

        df['person_index'] = utils.concatenate_person_index(df, self.matching_keys)
        df.set_index('person_index', drop=True, inplace=True)

        return df

    def write_matched_data(self, matches:pd.DataFrame) -> dict:
        self.cache.cache_matcher_data(df=matches, df_type='matcher_results')
        matched_results_paths = {}
        for event_type, primary_keys in self.schema_pk_lookup.items():
            if event_type in self.event_types_read:
                logger.info(f'Writing matched data for {event_type}')
                matched_results_paths[event_type] = self._write_one_event_type(
                    df=matches,
                    event_type=event_type,
                    primary_keys=primary_keys
                )
            else:
                logger.info(f'No data read for {event_type}. Skipping writing.')

        return matched_results_paths

    def _write_one_event_type(self, df:pd.DataFrame, event_type:str, primary_keys:list) -> str:
        # Join the matched ids to the source data
        df = self._join_matched_and_merged_data(df, event_type, primary_keys)

        # Cache the current match to S3
        logger.info(f'Writing data for {event_type}.')
        self.cache.cache_events(df=df, event_type=event_type)
        self.store.write_dataframe(df=df, path=f'{event_type}/matched')

        return f'{self.store.base_data_directory}/{event_type}/matched'

    def _join_matched_and_merged_data(
        self,
        right_df:pd.DataFrame,
        event_type:str,
        primary_keys:list
    ) -> pd.DataFrame:
        left_df=self._read_merged_data(event_type)[primary_keys]
        df = left_df.merge(
            right=right_df['matched_id'].to_frame(),
            left_index=True,
            right_index=True,
            copy=False,
            validate='many_to_one'
        )
        logger.info(f'Joined matched_ids to primary keys for {event_type}')

        return df

