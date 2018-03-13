#coding: utf-8

import os
import json
import ast

from flask import Flask, jsonify, request
from flask import make_response


from redis import Redis
from rq import Queue
from rq.job import Job

from dotenv import load_dotenv

import pandas as pd

import matcher.matcher as matcher
import matcher.contraster as contraster
import matcher.indexer as indexer
import matcher.utils as utils


# load dotenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

# load environment variables
S3_BUCKET = os.getenv('S3_BUCKET')
KEYS = ast.literal_eval(os.getenv('KEYS'))
INDEXER = os.getenv('INDEXER')
CONTRASTER = os.getenv('CONTRASTER')
CLUSTERING_PARAMS = {
    'eps': float(os.getenv('EPS')),
    'min_samples': int(os.getenv('MIN_SAMPLES')),
    'algorithm': os.getenv('ALGORITHM'),
    'leaf_size': int(os.getenv('LEAF_SIZE')),
    'n_jobs': int(os.getenv('N_JOBS')),
}
PG_CONNECTION = {
    'host': os.getenv('PGHOST'),
    'user': os.getenv('PGUSER'),
    'dbname': os.getenv('PGDATABASE'),
    'password': os.getenv('PGPASSWORD'),
    'port': os.getenv('PGPORT')
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


q = Queue(connection=redis_connection)


@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.DEBUG)


@app.route('/poke', methods=['GET'])
def poke():
    app.logger.info("I'm being poked!")
    return jsonify({
        'status': 'success',
        'message': 'Stop poking me!'
    })


@app.route('/match/<jurisdiction>/<event_type>', methods=['GET'])
def match(jurisdiction, event_type):
    upload_id = request.args.get('uploadId', None)
    if not upload_id:
        return jsonify(status='invalid', reason='uploadId not present')

    app.logger.debug("Someone wants to start a matching process!")

    job = q.enqueue_call(
        func=do_match,
        args=(jurisdiction, event_type),
        result_ttl=5000
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
            ),
            PG_CONNECTION)

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


@app.route('/list/<jurisdiction>', methods=['POST'])
def get_list(jurisdiction):
    app.logger.debug(f"Retrieving the list for the county {county}")
    if request.method == 'POST':
        try:
            data = request.get_json()
            start_date = data.get('start_date', '')
            end_date = data.get('end_date', '')
        except ValueError:
            return jsonify(f"Invalid date: ({start_date}, {end_date})")

        app.logger.debug(f"Filtering the list between dates {start_date} and {end_date}")

    return jsonify({
        'status': 'not implemented',
        'message': 'nice try, but we are still working on it'
    })


def do_match(jurisdiction, event_type):
    app.logger.info("Matching process started!")
    indexer_func = getattr(indexer, INDEXER)
    contraster_func = getattr(contraster, CONTRASTER)

    df = pd.concat([utils.load_data_for_matching(jurisdiction, event_type, S3_BUCKET, KEYS) for event_type in EVENT_TYPES])

    app.logger.info(f"Running matcher({KEYS},{INDEXER},{CONTRASTER})")
    df = matcher.run(
        df=df,
        keys=KEYS,
        indexer=indexer_func,
        contraster=contraster_func,
        clustering_params=CLUSTERING_PARAMS
    )

    for event_type in EVENT_TYPES:
        utils.write_matched_data(df, jurisdiction, event_type, S3_BUCKET, PG_CONNECTION)

    return {
        'status': 'done',
        'event_type': event_type,
        'message': 'matching proccess is done! check out the result!'
    }
