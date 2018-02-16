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
NEXT_EVENT_TYPES = {
    'hmis_service_stays': 'jail_bookings',
    'jail_bookings': 'hmis_service_stays'
}

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
        df = utils.read_matched_data_from_postgres(job.result['event_type'], PG_CONNECTION)

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

    # Read the data in and start the self-match process
    app.logger.info(f"Reading data from {S3_BUCKET}/{jurisdiction}/{event_type}")

    merged_key = f'csh/matcher/{jurisdiction}/{event_type}/merged'
    df1 = pd.read_csv(f's3://{S3_BUCKET}/{merged_key}', sep='|')

    app.logger.info(f"Running matcher({KEYS},{INDEXER},{CONTRASTER}) for self-match")
    df1, df2 = matcher.run(df1, KEYS, indexer_func, contraster_func, CLUSTERING_PARAMS)

    app.logger.info('Self-matching complete. Writing data to disk.')

    matched_key_1 = f'csh/matcher/{jurisdiction}/{event_type}/matched'
    utils.write_to_s3(df1, S3_BUCKET, matched_key_1)

    app.logger.info('Self-matches written to disk. Writing to database.')
    utils.write_matched_data_to_postgres(S3_BUCKET, matched_key_1, event_type, PG_CONNECTION)

    # Check if there is matched data available from the other source. If so,
    # match the two sets.
    app.logger.debug("Self-matching stored. Trying to match to other data source.")

    event_type_2 = NEXT_EVENT_TYPES[event_type]
    matched_key_2 = f'csh/matcher/{jurisdiction}/{event_type_2}/matched'

    try:
        app.logger.info(f"Trying to read data from {S3_BUCKET}/{jurisdiction}/{event_type_2}")
        df2 = pd.read_csv(f's3://{S3_BUCKET}/{matched_key_2}', sep='|')

        app.logger.info(f"Running matcher({KEYS},{INDEXER},{CONTRASTER}) to match two sources")
        df1, df2 = matcher.run(df1, KEYS, indexer_func, contraster_func, CLUSTERING_PARAMS, df2)

        app.logger.info('Matching between sources complete. Writing data to disk.')
        utils.write_to_s3(df1, S3_BUCKET, matched_key_1)
        utils.write_to_s3(df2, S3_BUCKET, matched_key_2)

        app.logger.info('Matches between sources written to disk. Writing to database.')
        utils.write_matched_data_to_postgres(S3_BUCKET, matched_key_1, event_type, PG_CONNECTION)
        utils.write_matched_data_to_postgres(S3_BUCKET, matched_key_2, event_type_2, PG_CONNECTION)

        app.logger.debug("Matching to other data scource done.")
    except FileNotFoundError:
        app.logger.debug("Matched data not available for other data source.")


    return {
        'status': 'done',
        'event_type': event_type,
        'message': 'matching proccess is done! check out the result!'
    }
