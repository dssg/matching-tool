# coding: utf-8

import os
import json

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

@app.route('/match/<jurisdiction>/<event_type>', methods=['GET'])
def match(jurisdiction, event_type):
    upload_id = request.args.get('uploadId', None)   ## QUESTION: Why is this a request arg and is not in the route? Also, Why in CamelCase?
    if not upload_id:
        return jsonify(status='invalid', reason='uploadId not present')

    logger.debug("Someone wants to start a matching process!")

    job = q.enqueue_call(
        func=do_match,
        args=(jurisdiction, event_type, upload_id),
        result_ttl=5000,
        timeout=100000,
        meta={'event_type': event_type}
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

    start_time = datetime.datetime.now()
    logger.info("Matching process started!")

    # Loading: collect matching data (keys) for all available event types & record which event types were found
    logger.info('Loading data for matching.')
    df, event_types_read = ioutils.load_data_for_matching(jurisdiction, upload_id)

    data_loaded_time = datetime.datetime.now()

    # Preprocessing: enforce data types and split/combine columns for feartures
    logger.info('Doing some preprocessing on the columns')
    df = preprocess.preprocess(df)
    data_preprocessed_time = datetime.datetime.now()

    logger.info(f"Running matcher")

    matches = matcher.run(df=df, clustering_params=CLUSTERING_PARAMS)
    data_matched_time = datetime.datetime.now()
    logger.debug('Matching done!')

    for key, matched in matches.items():
        logger.debug(f'Index of matches for {key}: {matched.index.values})')
        logger.debug(f'Columns of matches for {key}: {matched.columns.values}')

    logger.debug(f"Total matching time: {data_matched_time - start_time}")


    # Merging: Join the matched blocks into a single dataframe
    logger.info('Concatenating matched results!')
    all_matches = pd.concat(matches.values())
    matches_concatenated_time = datetime.datetime.now()

    logger.debug(f"Number of matched pairs: {len(all_matches)}")
    logger.debug(f"Total concatenating time: {matches_concatenated_time - data_matched_time}")

    # Writing: Join the matched ids to the source data for each event & write to S3 and postgres
    logger.info('Writing matched results!')
    ioutils.write_matched_data(all_matches, jurisdiction, event_types_read)
    data_written_time = datetime.datetime.now()

    total_match_time = data_written_time - start_time
    match_id = utils.unique_match_id()

    ioutils.insert_info_to_match_log(match_id, upload_id, start_time, data_written_time, total_match_time)

    return {
        'status': 'done',
        'number_of_matches_found': len(matches),
        'event_type': event_type,
        'jurisdiction': jurisdiction,
        'upload_id': upload_id,
        'message': 'matching proccess is done! check out the result!'
    }
