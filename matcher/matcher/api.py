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

@app.route('/match/<jurisdiction>', methods=['GET'])
def match(jurisdiction):
    upload_id = request.args.get('uploadId', None)   ## QUESTION: Why is this a request arg and is not in the route? Also, Why in CamelCase?
    if not upload_id:
        return jsonify(status='invalid', reason='uploadId not present')

    logger.debug("Someone wants to start a matching process!")

    job = q.enqueue_call(
        func=do_match,
        args=(jurisdiction, upload_id),
        result_ttl=5000,
        timeout=100000,
        meta={'upload_id': upload_id}
    )

    logger.info(f"Job id {job.get_id()}")

    return jsonify({"job": job.get_id()})


def do_match(jurisdiction, upload_id):

    match_job_id = utils.unique_match_job_id()
    match_start_time = datetime.datetime.now()
    logger.info("Matching process started!")

    try:
        # Loading: collect matching data (keys) for all available event types & record which event types were found
        logger.info('Loading data for matching.')
        df, event_types_read = ioutils.load_data_for_matching(jurisdiction, match_job_id)

        data_loaded_time = datetime.datetime.now()

        # Preprocessing: enforce data types and split/combine columns for feartures
        logger.info('Doing some preprocessing on the columns')
        df = preprocess.preprocess(df, match_job_id, jurisdiction)
        data_preprocessed_time = datetime.datetime.now()

        # Matching: block the data, generate pairs and features, and cluster entities
        logger.info(f"Running matcher")
        matches = matcher.run(df=df, clustering_params=CLUSTERING_PARAMS, jurisdiction=jurisdiction, match_job_id=match_job_id, blocking_rules=BLOCKING_RULES)
        data_matched_time = datetime.datetime.now()
        logger.debug('Matching done!')

        for key, matched in matches.items():
            logger.debug(f'Index of matches for {key}: {matched.index.values})')
            logger.debug(f'Columns of matches for {key}: {matched.columns.values}')

        logger.debug(f"Total matching time: {data_matched_time - match_start_time}")

        # Merging: Join the matched blocks into a single dataframe
        logger.info('Concatenating matched results!')
        all_matches = pd.concat(matches.values())
        matches_concatenated_time = datetime.datetime.now()

        logger.debug(f"Number of matched pairs: {len(all_matches)}")
        logger.debug(f"Total concatenating time: {matches_concatenated_time - data_matched_time}")

        # Writing: Join the matched ids to the source data for each event & write to S3 and postgres
        logger.info('Writing matched results!')
        ioutils.write_matched_data(all_matches, jurisdiction, match_job_id, event_types_read)
        data_written_time = datetime.datetime.now()

        total_match_time = data_written_time - match_start_time

        ioutils.insert_info_to_match_log(match_job_id, upload_id, match_start_time, data_written_time, True, total_match_time)
        logger.info('Finished')

        return {
            'status': 'done',
            'number_of_matches_found': len(matches),
            'jurisdiction': jurisdiction,
            'upload_id': upload_id,
            'message': 'matching proccess is done! check out the result!'
        }
    except:
        match_fail_time = datetime.datetime.now()
        total_match_time = match_fail_time - match_start_time
        ioutils.insert_info_to_match_log(match_job_id, upload_id, match_start_time, match_fail_time, False, total_match_time)

        return {
            'status': 'failed',
            'number_of_matches_found': None,
            'upload_id': upload_id,
            'message': 'matching proccess failed...'
        }
