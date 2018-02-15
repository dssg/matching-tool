from flask import render_template, request, jsonify, Blueprint, url_for, send_file
import pandas as pd
import datetime
import json
import copy
from collections import OrderedDict
import webapp.apis.query
from webapp.apis import query

chart_api = Blueprint('chart_api', __name__, url_prefix='/api/chart')


SAMPLE_DATA_DIR = 'sample_data/results_input/'

@chart_api.route('/get_schema', methods=['GET'])
def get_records_by_time():
    start = request.args.get('start')
    end = request.args.get('end')
    records = query.get_records_by_time(start, end)
    return jsonify(results=records)

@chart_api.route('/download/<string:to_be_downloaded>', methods=['GET'])
def download_list(to_be_downloaded):
    if to_be_downloaded == "chart":
        return send_file('static/files/chart_2017-11-01_t0_2017-11-30.png', as_attachment=True)
    else:
        return send_file('static/files/2017-11-01_to_2017-11-30.csv', as_attachment=True)
