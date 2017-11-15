#coding: utf-8

from flask import Flask, jsonify, request


import matcher.matcher as matcher
import matcher.contraster as contraster
import matcher.indexer as indexer

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


@app.route('/match')
def match():
    app.logger.debug("Someone wants to start a matching process!")
    ## df = read data from s3 and returning a pd.DataFrame
    #keys = [] ## List of columns to be the key
    #indexer = indexer.identity
    #contraster = contraster.exact
    #df = matcher.run(df, keys, indexer, contraster)
    app.logger.debug("Beeep...booop")
    app.logger.debug("We did the match")
    return jsonify({
        'status':'not implemented',
        'message':'nice try, but we are still working on it'
    })

@app.route('/list/<county>', methods=['GET', 'POST'])
def get_list(county):
    app.logger.debug(f"Retriving the list for the county {county}")
    start_date = request.form.get('start_date', '')
    end_date = request.form.get('end_date', '')
    app.logger.debug(f"Filtering the list between dates {start_date} and {end_date}")
    return jsonify({
        'status': 'not implemented',
        'message': 'nice try, but we are still working on it'
    })


