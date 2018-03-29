#coding: utf-8

import os
import json
import ast

from flask import Flask, jsonify, request
from flask import make_response

import time

from rq.registry import StartedJobRegistry
from redis import Redis
from rq import Queue
from rq.job import Job

from dotenv import load_dotenv

import pandas as pd

import matcher.matcher as matcher
import matcher.preprocess as preprocess
import matcher.utils as utils

# load dotenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

# load environment variables
KEYS = ast.literal_eval(os.getenv('KEYS'))
CLUSTERING_PARAMS = {
    'eps': float(os.getenv('EPS')),
    'min_samples': int(os.getenv('MIN_SAMPLES')),
    'algorithm': os.getenv('ALGORITHM'),
    'leaf_size': int(os.getenv('LEAF_SIZE')),
    'n_jobs': int(os.getenv('N_JOBS')),
}

# Lookups
EVENT_TYPES = [
    'hmis_service_stays', 
    'jail_bookings'
]

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
    app.logger.info(f"queue: {queued_jobs}")

    return jsonify({
        'q': len(q),
        'job_ids': queued_job_ids,
        'current_job': registry.get_job_ids(),
        'expired_job_id':  registry.get_expired_job_ids(),
        'enqueue_at': [job.enqueued_at for job in queued_jobs]
    })

@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.DEBUG)

@app.route('/match/<jurisdiction>/<event_type>', methods=['GET'])
def match(jurisdiction, event_type):
    upload_id = request.args.get('uploadId', None)   ## QUESTION: Why is this a request arg and is not in the route? Also, Why in CamelCase?
    if not upload_id:
        return jsonify(status='invalid', reason='uploadId not present')

    app.logger.debug("Someone wants to start a matching process!")

    job = q.enqueue_call(
        func=do_match,
        args=(jurisdiction, event_type, upload_id),
        result_ttl=5000,
        timeout=100000
    )

    app.logger.info(f"Job id {job.get_id()}")

    return jsonify({"job": job.get_id()})


@app.route('/match/results/<job_key>', methods=["GET"])
def get_match_results(job_key):
    job = Job.fetch(job_key, connection=redis_connection)
    app.logger.info(job.result)
    if job.is_finished:
        df = utils.read_matched_data_from_postgres(
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


    start_time = time.time()
    
    app.logger.info("Matching process started!")

    # We will frame the record linkage problem as a deduplication problem
    app.logger.info('Loading data for matching.')
    df = pd.concat([utils.load_data_for_matching(jurisdiction, event_type, upload_id, KEYS) for event_type in EVENT_TYPES])

    app.logger.info('Doing some preprocessing on the columns')
    df = preprocess.preprocess(df)
    app.logger.info(f"Races observed in preprocessed df: {df['race']}")

    app.logger.info(f"Running matcher({KEYS})")
    app.logger.debug(f"The dataframe has the following columns: {df.columns}")
    app.logger.debug(f"The dimensions of the dataframe is: {df.shape}")
    app.logger.debug(f"The indices are {df.index}")
    app.logger.debug(f'df has {len(df)} rows and {len(df.index.unique())} unique indices')
    app.logger.debug(f'The dataframe has the following duplicate indices: {df[df.index.duplicated()].index.values}')

    matches = matcher.run(df=df, clustering_params=CLUSTERING_PARAMS)
    app.logger.debug('Matching done!')

    for key, matched in matches.items():
        app.logger.debug(f'Index of matches for {key}: {matched.index.values})')
        app.logger.debug(f'Columns of matches for {key}: {matched.columns.values}')

    app.logger.info('Writing matched results!')

    # Merging the dataframe

    end_time_1 = time.time()

    app.logger.debug(f"Total matching time: {end_time_1 - start_time}")
    
    all_matches = pd.concat(matches.values())

    end_time_2 = time.time()

    app.logger.debug(f"Number of matched pairs: {len(all_matches)}")

    app.logger.debug(f"Total concatenating time: {end_time_2 - end_time_1}")
    
    #for e_type in EVENT_TYPES:
    #    utils.write_matched_data(all_matches, jurisdiction, e_type)

    return {
        'status': 'done',
        'number_of_matches_found': len(matches),
        'event_type': event_type,
        'jurisdiction': jurisdiction,
        'upload_id': upload_id,
        'message': 'matching proccess is done! check out the result!'
    }
