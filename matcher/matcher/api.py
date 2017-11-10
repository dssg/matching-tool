#coding: utf-8

from flask import Flask, jsonify

app = Flask(__name__)


# set config environment
app.config.from_object(__name__)

app.config.update(dict(
    ))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def index():
    return jsonify({
        'status': 'success',
        'message': 'Zzzzzzz'
        })


@app.route('/poke', methods=['GET'])
def poke():
    return jsonify({
        'status': 'success',
        'message': 'Stop poking me!'
        })


