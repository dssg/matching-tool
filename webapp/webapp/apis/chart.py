from flask import render_template, request, jsonify, Blueprint, url_for, send_file, make_response
import pandas as pd
import datetime
import json
import copy
from collections import OrderedDict
import webapp.apis.query
from webapp.apis import query

chart_api = Blueprint('chart_api', __name__, url_prefix='/api/chart')


SAMPLE_DATA_DIR = 'sample_data/results_input/'
global current_list
current_list = None

@chart_api.route('/get_schema', methods=['GET'])
def get_records_by_time():
    start = request.args.get('start')
    end = request.args.get('end')
    records = query.get_records_by_time(start, end)
    global current_list
    current_list = records
    return jsonify(results=records)

@chart_api.route('/download_list', methods=['GET'])
def download_list():
	global current_list
	df = pd.DataFrame(current_list['filteredData']['tableData'])
	output = make_response(df.to_csv(index=False))
	output.headers["Content-Disposition"] = "attachment; filename=export.csv"
	output.headers["Content-type"] = "text/csv"
	return output
