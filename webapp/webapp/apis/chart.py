from flask import abort, request, jsonify, Blueprint, make_response, Response
from flask_security import login_required
from webapp.logger import logger
import pandas as pd
from webapp.apis import query
from webapp.users import can_upload_file

chart_api = Blueprint('chart_api', __name__, url_prefix='/api/chart')


@chart_api.route('/get_schema', methods=['GET'])
@login_required
def get_records_by_time():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    jurisdiction = request.args.get('jurisdiction')
    limit = request.args.get('limit', 10)
    offset = request.args.get('offset', 0)
    order_column = request.args.get('orderColumn')
    order = request.args.get('order')
    set_status = request.args.get('setStatus')
    logger.info(f'Pulling data from {start_date} to {end_date}')
    records = query.get_records_by_time(
        start_date,
        end_date,
        jurisdiction,
        limit,
        offset,
        order_column,
        order,
        set_status
    )
    return jsonify(results=records)


@chart_api.route('/download_list', methods=['GET'])
@login_required
def download_list():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    jurisdiction = request.args.get('jurisdiction')
    limit = 'ALL'
    offset = 0
    order_column = request.args.get('orderColumn')
    order = request.args.get('order')
    set_status = request.args.get('setStatus')
    records = query.get_records_by_time(
        start_date,
        end_date,
        jurisdiction,
        limit,
        offset,
        order_column,
        order,
        set_status
    )
    df = pd.DataFrame(records['filteredData']['tableData'])
    output = make_response(df.to_csv(index=False))
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@chart_api.route('/download_source', methods=['GET'])
@login_required
def download_source():
    jurisdiction = request.args.get('jurisdiction')
    event_type = request.args.get('eventType')
    if not can_upload_file(jurisdiction, event_type):
        return abort(403)
    source_data_filehandle = query.source_data_to_filehandle(jurisdiction, event_type)
    output = Response(source_data_filehandle, mimetype='text/csv')
    output.headers["Content-Disposition"] = "attachment; filename={}.csv".format(event_type)
    output.headers["Content-type"] = "text/csv"
    return output


@chart_api.route('/last_upload_date', methods=['GET'])
@login_required
def get_last_upload_date():
    last_upload = query.last_upload_date()
    try:
        assert len(last_upload) == 1
        last_upload_date = last_upload[0]['upload_start_time']
        logger.info(type(last_upload_date))
        last_upload_date = last_upload_date.strftime('%Y-%m-%d')
        return jsonify(results=last_upload_date)
    except:
        return jsonify("no valid upload date")
