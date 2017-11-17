from flask import render_template, request, jsonify, Blueprint
import pandas as pd
import datetime
import json

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

@chart_api.route('/test_chart_api', methods=['GET'])
def test():
    return jsonify(result='test')
