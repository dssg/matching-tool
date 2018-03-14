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
import matcher.utils as utils

# load dotenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

# load environment variables
KEYS = ast.literal_eval(os.getenv('KEYS'))


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



@app.route('/match/<jurisdiction>/<event_type>', methods=['GET'])
def match(jurisdiction, event_type):
    upload_id = request.args.get('uploadId', None)   ## QUESTION: Why is this a request arg and is not in the route? Also, Why in CamelCase?
    if not upload_id:
        return jsonify(status='invalid', reason='uploadId not present')

    app.logger.debug("Someone wants to start a matching process!")

    job = q.enqueue_call(
        func=do_match,
        args=(jurisdiction, event_type, upload_id),
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
    app.logger.info("Matching process started!")
    
    df = pd.concat([utils.load_data_for_matching(jurisdiction, event_type, upload_id, KEYS) for event_type in EVENT_TYPES])

    app.logger.info(f"Running matcher({KEYS})")
    app.logger.debug(f"The dataframe has the following columns: {df.columns}")
    app.logger.debug(f"The dimensions of the dataframe is: {df.shape}")
    app.logger.debug(f"The indices are {df.index}")
        
    df = matcher.run(df=df, keys=KEYS)

    # for event_type in EVENT_TYPES:
    #     utils.write_matched_data(df, jurisdiction, event_type)

    app.logger.debug(f"Returned dataframe has the following columns: {df.columns}")
    app.logger.debug(f"The dimensions of the returned dataframe is: {df.shape}")
    app.logger.debug(f"The indices are {df.index}")    
    
    return {
        'status': 'done',
        'event_type': event_type,
        'jurisdiction': jurisdiction,
        'message': 'matching proccess is done! check out the result!'
    }
