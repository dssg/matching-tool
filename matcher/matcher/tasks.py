# coding: utf-8

__version__='0.0.1'


import os

import datetime
import pandas as pd
import yaml

import matcher.pipeline as pipeline
import matcher.preprocess as preprocess
import matcher.utils as utils
import matcher.storage as storage

from matcher.logger import logger

from redis import Redis
from rq import Queue
redis_connection = Redis(host='redis', port=6379)
q = Queue('webapp', connection=redis_connection)


def do_match(
    base_data_directory:str,
    schema_pk_lookup:dict,
    upload_id:str=None,
    notify_webapp:bool=True,
    config_path:str='matcher_config.yaml'
):
    # Initializing: let's get started by collecting some job metadata and creating storage objects
    with open(config_path) as f:
        config = yaml.load(f)
    logger.debug(config)    
    metadata = {
        'match_job_start_time': datetime.datetime.now(),
        'match_job_id': utils.unique_match_job_id(),
        'base_data_directory': base_data_directory,
        'config': config
    }
    logger.info('Matching process started!')

    store = storage.Store(base_data_directory)
    cache = storage.Cache(store, metadata['match_job_id'], **config['cache'])
    matcher_service_store = storage.MatcherServiceStore(store, cache, schema_pk_lookup, config['keys'])

    try:
        # Loading: collect matching data (keys) for all available event types & record which event types were found
        logger.info('Loading data for matching.')
        df = matcher_service_store.load_data_for_matching()
        metadata['event_types_read'] = matcher_service_store.event_types_read
        metadata['loaded_data_columns'] = list(df.columns.values)
        metadata['loaded_data_shape'] = list(df.shape)
        metadata['data_loaded_time'] = datetime.datetime.now()

        # Preprocessing: enforce data types and split/combine columns for feartures
        logger.info('Doing some preprocessing on the columns')
        df = preprocess.preprocess(df, cache)
        metadata['preprocessed_data_columns'] = list(df.columns.values)
        metadata['preprocessed_data_shape'] = list(df.shape)
        metadata['data_preprocessed_time'] = datetime.datetime.now()

        # Record Linkage: block the data, generate pairs and features, and cluster entities
        logger.info(f'Running matching pipeline.')
        matchmaker = pipeline.Pipeline(config=config)
        matchmaker.run(df)
        matches = matchmaker.matches
        metadata['data_matched_time'] = datetime.datetime.now()
        logger.debug('Matching done!')

        logger.debug(f'Number of matched pairs: {len(matches)}')

        # Writing: Join the matched ids to the source data for each event & write to S3 and postgres
        logger.info('Writing matched results!')
        matched_results_paths = matcher_service_store.write_matched_data(matches=matches)
        metadata['data_written_time'] = datetime.datetime.now()
        #ioutils.write_dict_to_yaml(metadata, f'{base_data_directory}/match_cache/metadata/{metadata["match_job_id"]}')

        logger.info('Finished successfully!')
        match_end_time = datetime.datetime.now()
        match_runtime =  match_end_time - metadata['match_job_start_time']

        match_successful = True
        status_message = 'new matches are available. Yipee!'

    except Exception as e:
        match_end_time = datetime.datetime.now()
        match_run_time = match_end_time - metadata['match_job_start_time']
        match_successful = False
        status_message = 'matching failed. SAD!'
        try:
            matched_results_paths
        except NameError:
            matched_results_paths = None

        try:
            match_end_time
        except NameError:
            match_end_time = datetime.datetime.now()

        try:
            match_runtime
        except NameError:
            match_runtime = match_end_time - metadata['match_job_start_time']

        logger.error(f'Matcher failed with message "{str(e)}"')

    finally:
        if notify_webapp:
            job = q.enqueue_call(
                func='webapp.match_finished',
                args=(
                    matched_results_paths,
                    metadata['match_job_id'],
                    metadata['match_job_start_time'],
                    match_end_time,
                    match_successful,
                    match_runtime,
                    upload_id
                ),
                result_ttl=5000,
                timeout=3600
            )
            logger.info(f'Notified the webapp that {status_message}')
        logger.info('Matcher done!!')

