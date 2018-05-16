# coding: utf-8

import os
import json
import ast

from flask import Flask, jsonify, request
from flask import make_response

import datetime

from rq.registry import StartedJobRegistry
from redis import Redis
from rq import Queue, get_current_job
from rq.job import Job
from rq.registry import StartedJobRegistry

from dotenv import load_dotenv

import pandas as pd

import matcher.matcher as matcher
import matcher.preprocess as preprocess
import matcher.utils as utils
import matcher.ioutils as ioutils

from matcher.logger import logger

# load dotenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

# load environment variables
CLUSTERING_PARAMS = {
    'eps': float(os.getenv('EPS')),
    'min_samples': int(os.getenv('MIN_SAMPLES')),
    'algorithm': os.getenv('ALGORITHM'),
    'leaf_size': int(os.getenv('LEAF_SIZE')),
    'n_jobs': int(os.getenv('N_JOBS')),
}
BLOCKING_RULES = ast.literal_eval(os.getenv('BLOCKING_RULES'))


# Initialize the app
app = Flask(__name__)
redis_connection = Redis(host='redis', port=6379)

# set config environment
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTINGS', silent=True)


q = Queue('matching', connection=redis_connection)
registry = StartedJobRegistry('matching', connection=redis_connection)

@app.route('/match/get_jobs')
def list_jobs():
    queued_job_ids = q.job_ids
    queued_jobs = q.jobs
    logger.info(f"queue: {queued_jobs}")

    return jsonify({
	'q': len(q),
	'job_ids': queued_job_ids,
	'current_job': registry.get_job_ids(),
	'expired_job_id':  registry.get_expired_job_ids(),
	'enqueue_at': [job.enqueued_at for job in queued_jobs]
    })

@app.route('/match/<jurisdiction>/<event_type>/<filename>', methods=['GET'])
def match(jurisdiction, event_type, filename):
    upload_id = request.args.get('uploadId', None)   ## QUESTION: Why is this a request arg and is not in the route? Also, Why in CamelCase?
    if not upload_id:
        return jsonify(status='invalid', reason='uploadId not present')

    logger.debug("Someone wants to start a matching process!")

    job = q.enqueue_call(
        func=do_match,
        args=(jurisdiction, event_type, upload_id),
        result_ttl=5000,
        timeout=100000,
        meta={'event_type': event_type, 'filename': filename}
    )

    logger.info(f"Job id {job.get_id()}")

    return jsonify({"job": job.get_id()})


@app.route('/match/results/<job_key>', methods=["GET"])
def get_match_results(job_key):
    job = Job.fetch(job_key, connection=redis_connection)
    logger.info(job.result)
    if job.is_finished:
        df = ioutils.read__data_from_postgres(
            utils.get_matched_table_name(
            event_type=job.result['event_type'],
            jurisdiction=job.result['jurisdiction']
    ))

        response = make_response(jsonify(df.to_json(orient='records')))
        response.headers["Content-Type"] = "text/json"

        return response

    else:
        return jsonify({
            'status': 'not yet',
            'message': 'nice try, but we are still working on it'
        })


@app.route('/match/job_finished/<job_key>', methods=["GET"])
def get_match_finished(job_key):
    job = Job.fetch(job_key, connection=redis_connection)
    if job.is_finished:
        return jsonify(job.result)
    else:
        return jsonify({
            'status': 'not yet',
            'message': 'nice try, but we are still working on it'
        })


def do_match(jurisdiction, event_type, upload_id):
    # Initializing: let's get started by collecting some job metadata
    metadata = {
        'match_job_start_time': datetime.datetime.now(),
        'match_job_id': utils.unique_match_job_id(),
        'jurisdiction': jurisdiction,
        'clustering_params': CLUSTERING_PARAMS,
        'blocking_rules': BLOCKING_RULES
    }
    logger.info("Matching process started!")

    # Loading: collect matching data (keys) for all available event types & record which event types were found
    logger.info('Loading data for matching.')
    df, event_types_read = ioutils.load_data_for_matching(jurisdiction, metadata['match_job_id'])
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
        clustering_params=CLUSTERING_PARAMS,
        jurisdiction=jurisdiction,
        blocking_rules=BLOCKING_RULES,
        match_job_id=metadata['match_job_id']
    )
    logger.debug('Initialized matcher object')
    matches = match_object.block_and_match(df=df)
    metadata['data_matched_time'] = datetime.datetime.now()
    metadata.update(match_object.metadata)
    logger.debug('Matching done!')

    for key, matched in matches.items():
        logger.debug(f'Index of matches for {key}: {matched.index.values})')
        logger.debug(f'Columns of matches for {key}: {matched.columns.values}')

    logger.debug(f"Time from initializing to matches: {metadata['data_matched_time'] - metadata['match_job_start_time']}")

    # Merging: Join the matched blocks into a single dataframe
    logger.info('Concatenating matched results!')
    all_matches = pd.concat(matches.values())
    metadata['num_matched_pairs'] = len(all_matches)
    metadata['matches_concatenated_time'] = datetime.datetime.now()

    logger.debug(f"Number of matched pairs: {metadata['num_matched_pairs']}")
    logger.debug(f"Total concatenating time: {metadata['matches_concatenated_time'] - metadata['data_matched_time']}")

    # Writing: Join the matched ids to the source data for each event & write to S3 and postgres
    logger.info('Writing matched results!')
    ioutils.write_matched_data(all_matches, jurisdiction, metadata['match_job_id'], metadata['event_types_read'])
    metadata['data_written_time'] = datetime.datetime.now()

    total_match_time = metadata['data_written_time'] - metadata['match_job_start_time']
    logger.info(f'Total time for pipeline: {total_match_time}')
    ioutils.write_dict_to_yaml(metadata, f"csh/matcher/{jurisdiction}/match_cache/metadata/{metadata['match_job_id']}")

    ioutils.insert_info_to_match_log(
        id=metadata['match_job_id'],
        upload_id=upload_id,
        match_start_timestamp=metadata['match_job_start_time'],
        match_complete_timestamp=metadata['data_written_time'],
        runtime=total_match_time
    )
    logger.info('Finished')

    return {
        'status': 'done',
        'number_of_matches_found': len(all_matches),
        'event_type': event_type,
        'jurisdiction': jurisdiction,
        'upload_id': upload_id,
        'message': 'matching proccess is done! check out the result!'
    }
