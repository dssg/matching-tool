from flask import render_template, request, jsonify, Blueprint, url_for, send_file
import pandas as pd
import datetime
import json
import copy
from collections import OrderedDict

chart_api = Blueprint('chart_api', __name__, url_prefix='/api/chart')



@chart_api.route('/get_table_data', methods=['GET'])
def get_table_data():
    table = json.load(open('table.json'))['table']
    return jsonify(result=table)

@chart_api.route('/get_homeless_bar_data', methods=['GET'])
def get_homeless_bar_data():
    homeless_bar_data = json.load(open('homeless_bar_data.json'))['homeless_bar_data']
    return jsonify(result=homeless_bar_data)

@chart_api.route('/get_jail_bar_data', methods=['GET'])
def get_jail_bar_data():
    jail_bar_data = json.load(open('jail_bar_data.json'))['jail_bar_data']
    return jsonify(result=jail_bar_data)

@chart_api.route('/get_venn_diagram_data', methods=['GET'])
def get_venn_diagram_data():
    venn_diagram_data =  json.load(open('venn_diagram_data.json'))['venn_diagram_data']
    return jsonify(result=venn_diagram_data)

@chart_api.route('/get_full_json_for_view1', methods=['GET'])
def get_full_json_for_view1():
    data = OrderedDict(json.load(open('webapp_schema.json'), object_pairs_hook=OrderedDict))
    print(data)
    return json.dumps({"result": data})

@chart_api.route('/get_full_json_for_view2', methods=['GET'])
def get_full_json_for_view2():
    data = OrderedDict(json.load(open('webapp_schema2.json'), object_pairs_hook=OrderedDict))
    print(data)
    return json.dumps({"result": data})

@chart_api.route('/download/<string:to_be_downloaded>', methods=['GET'])
def download_list(to_be_downloaded):
    # return redirect("https://raw.githubusercontent.com/dssg/csh/master/bookings-fake-1.csv?token=AJNBj83w8eligJ8oofIhKs6Tq46hC4ncks5aGEQOwA%3D%3D")
    # return url_for('static', filename='downloads/2017-10-01_2017-10-31_all.csv')
    if to_be_downloaded == "chart":
        return send_file('static/downloads/chart_2017-10-01_to_2017-10-31.png', as_attachment=True)
    else:
        return send_file('static/downloads/2017-10-01_to_2017-10-31.csv', as_attachment=True)
