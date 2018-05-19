# coding: utf-8

__version__='0.0.1'


import os
import ast

import datetime
import pandas as pd

import matcher.matcher as matcher
import matcher.preprocess as preprocess
import matcher.utils as utils
import matcher.ioutils as ioutils

from matcher.logger import logger


# load environment variables
CLUSTERING_PARAMS = {
    'eps': float(os.getenv('EPS')),
    'min_samples': int(os.getenv('MIN_SAMPLES')),
    'algorithm': os.getenv('ALGORITHM'),
    'leaf_size': int(os.getenv('LEAF_SIZE')),
    'n_jobs': int(os.getenv('N_JOBS')),
}
BLOCKING_RULES = ast.literal_eval(os.getenv('BLOCKING_RULES'))


def do_match(base_data_directory:str, schema_pk_lookup:dict, upload_id=None):
     # Initializing: let's get started by collecting some job metadata
     metadata = {
         'match_job_start_time': datetime.datetime.now(),
         'match_job_id': utils.unique_match_job_id(),
         'jurisdiction': jurisdiction,
         'clustering_params': CLUSTERING_PARAMS,
         'blocking_rules': BLOCKING_RULES
     }
    logger.info("Matching process started!")

    try:
        # Loading: collect matching data (keys) for all available event types & record which event types were found
        logger.info('Loading data for matching.')
        df, event_types_read = ioutils.load_data_for_matching(base_data_directory, schema_pk_lookup.keys(), metadata['match_job_id'])
        metadata['event_types_read'] = list(event_types_read)
        metadata['loaded_data_columns'] = list(df.columns.values)
        metadata['loaded_data_shape'] = list(df.shape)
        metadata['data_loaded_time'] = datetime.datetime.now()

        # Preprocessing: enforce data types and split/combine columns for feartures
        logger.info('Doing some preprocessing on the columns')
        df = preprocess.preprocess(df, metadata['match_job_id'], jurisdiction)
        metadata['preprocessed_data_columns'] = list(df.columns.values)
        metadata['preprocessed_data_shape'] = list(df.shape)
        metadata['data_preprocessed_time'] = datetime.datetime.now()

        # Matching: block the data, generate pairs and features, and cluster entities
        logger.info(f"Running matcher")
        match_object = matcher.Matcher(
            jurisdiction=jurisdiction,
            match_job_id=metadata['match_job_id']
            clustering_rules=CLUSTERING_RULES,
            contrast_rules=CONTRAST_RULES,
            blocking_rules=BLOCKING_RULES,
        )
        matches = match_object.block_and_match(df=df)
        metadata['data_matched_time'] = datetime.datetime.now()
        metadata.update(match_object.metadata)
        logger.debug('Matching done!')

        logger.debug(f"Number of matched pairs: {len(all_matches)}")
        logger.debug(f"Total concatenating time: {matches_concatenated_time - data_matched_time}")

        # Writing: Join the matched ids to the source data for each event & write to S3 and postgres
        logger.info('Writing matched results!')
        matched_results_paths = ioutils.write_matched_data(
            matches=matches,
            base_data_directory=base_data_directory,
            schema_pk_lookup={schema_pk_lookup[event_type] for event_type in event_types_read},
            match_job_id=match_job_id
        )
        metadata['data_written_time'] = datetime.datetime.now()
        ioutils.write_dict_to_yaml(metadata, f"csh/matcher/{jurisdiction}/match_cache/metadata/{metadata['match_job_id']}")

        logger.info('Finished')
        match_end_time = datetime.datetime.now()
        match_runtime =  match_end_time - metadata['match_job_start_time']
        
        webapp.match_finished(
            matched_results_paths=matched_results_paths,
            match_job_id=metadata['match_job_id'],
            match_start_at=metadata['match_job_start_time'],
            match_complete_at=match_end_time,
            match_status=True,
            match_runtime=match_runtime,
            upload_id=upload_id
        )

    except Exception as e:
        logger.error(f'Matcher failed with message "{e.message}"')
        match_fail_time = datetime.datetime.now()
        match_run_time = match_fail_time - metadata['match_job_start_time']

        webapp.match_finished(
            matched_results_paths={},
            match_job_id=metadata['match_job_id'],
            match_start_at=metadata['match_job_start_time'],
            match_complete_at=match_fail_time,
            match_status=False,
            match_runtime=match_runtime,
            upload_id=upload_id
        )

