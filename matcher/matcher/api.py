#coding: utf-8

import os
import json
import ast

from flask import Flask, jsonify, request
from flask import make_response

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

# Initialize the app
app = Flask(__name__)

# set config environment
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTINGS', silent=True)


@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.DEBUG)



@app.route('/')
def index():
    return jsonify({
        'status': 'success',
        'message': 'I am here, hi!'
    })


@app.route('/poke', methods=['GET'])
def poke():
    app.logger.info("I'm being poked!")
    return jsonify({
        'status': 'success',
        'message': 'Stop poking me!'
    })


@app.route('/match/<jurisdiction>/<event_type>', methods=['GET'])
def match(jurisdiction, event_type):
    # TODO
    # for now, just matches within the passed event type, but eventually,
    # it should follow that step by checking for a matched version of the other
    # event type and then matching to that
    app.logger.debug("Someone wants to start a matching process!")

    app.logger.info(f"Reading data from {S3_BUCKET}/{jurisdiction}")

    merged_key = f'csh/matcher/{jurisdiction}/{event_type}/merged'
    df1 = pd.read_csv(f's3://{S3_BUCKET}/{merged_key}', sep='|')

    indexer_func = getattr(indexer, INDEXER)
    contraster_func = getattr(contraster, CONTRASTER)

    app.logger.info(f"Running matcher({KEYS},{INDEXER},{CONTRASTER})")
    app.logger.debug("Beeep...booop")
    df1, df2 = matcher.run(df1, KEYS, indexer_func, contraster_func, CLUSTERING_PARAMS)
    matched_key_1 = f'csh/matcher/{jurisdiction}/{event_type}/matched'
    utils.write_to_s3(df1, S3_BUCKET, matched_key_1)

    app.logger.debug("Internal matching done. Trying to match to other data source.")

    if event_type == 'hmis':
        event_type_2 = 'bookings'
    elif event_type == 'bookings':
        event_type_2 = 'hmis'
    matched_key_2 = f'csh/matcher/{jurisdiction}/{event_type_2}/matched'
    try:
        df2 = pd.read_csv(f's3://{S3_BUCKET}/{matched_key_2}', sep='|')
        df1, df2 = matcher.run(df1, KEYS, indexer_func, contraster_func, CLUSTERING_PARAMS, df2)
        utils.write_to_s3(df1, S3_BUCKET, matched_key_1)
        utils.write_to_s3(df2, S3_BUCKET, matched_key_2)
        app.logger.debug("Matching to other data scource done.")
    except FileNotFoundError:
        app.logger.debug("Matched data not available for other data source.")

    response = make_response(df2.to_json(orient='records'))
    response.headers["Content-Type"] = "text/json"
    return response
    

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


