from flask import make_response, request, jsonify, Blueprint
from flask_security import login_required
from flask_login import current_user

from webapp.logger import logger
from webapp.database import db_session
from webapp.models import Upload, MergeLog
from webapp.tasks import \
    upload_to_s3,\
    sync_upload_metadata,\
    copy_raw_table_to_db,\
    upsert_raw_table_to_master,\
    sync_merged_file_to_s3,\
    add_missing_fields,\
    validate_file,\
    validate_header,\
    bootstrap_matched_tables
from webapp.users import can_upload_file, get_jurisdiction_roles
from webapp.utils import s3_upload_path, notify_matcher, infer_delimiter, unique_upload_id

from werkzeug.utils import secure_filename

from redis import Redis
from rq import Queue
from rq.job import Job

from collections import defaultdict
import re
import unicodecsv as csv
import os
from functools import partial
from datetime import datetime

upload_api = Blueprint('upload_api', __name__, url_prefix='/api/upload')


def get_q(redis_connection):
    return Queue('webapp', connection=redis_connection)


def get_redis_connection():
    return Redis(host='redis', port=6379)


def get_sample(saved_filename):
    delimiter = infer_delimiter(saved_filename)
    with open(saved_filename, 'rb') as request_file:
        reader = csv.DictReader(request_file, delimiter=delimiter)
        sample_rows = []
        for x in range(10):
            try:
                sample_rows.append(next(reader))
            except StopIteration:
                break
        return sample_rows, reader.fieldnames


def can_access_file(upload_id):
    upload = db_session.query(Upload).get(upload_id)
    if not upload:
        raise ValueError(
            'upload_id: %s not present in metadata database',
            upload_id
        )
    logger.info(
        'Found jurisdiction %s and event type %s for upload id %s',
        upload.jurisdiction_slug,
        upload.event_type_slug,
        upload_id
    )
    return can_upload_file(upload.jurisdiction_slug, upload.event_type_slug)


def format_validation_report(report, event_type_slug):
    error_summary = defaultdict(dict)
    headers = report['tables'][0]['headers']
    for error in report['tables'][0]['errors']:
        message = re.sub('row \d+ and', '', error['message'])
        message = re.sub('Row number \d+: ', '', message)
        match = re.search('The value (.*) in ', message)
        value = ''
        if match:
            value = match.group(1)
            message = re.sub(re.escape(value), '', message, count=1)
        if error['column-number']:
            column_number = error['column-number'] - 1
            field_name = headers[column_number]
        else:
            field_name = ''
        if (field_name, message) not in error_summary:
            error_summary[(field_name, message)] = dict(row_numbers=[], values=set())
        error_summary[(field_name, message)]['row_numbers'].append(error['row-number'])
        if value and value not in error_summary[(field_name, message)]:
            error_summary[(field_name, message)]['values'].add(value)

    return [dict(
        field_name=field_name,
        message=message,
        num_rows=len(data['row_numbers']),
        values=list(data['values'])[0:100],
        row_numbers=data['row_numbers']
    ) for (field_name, message), data in error_summary.items()]


@upload_api.route('/jurisdictional_roles.json', methods=['GET'])
@login_required
def jurisdiction_roles():
    return jsonify(results=get_jurisdiction_roles())


@upload_api.route('/validated_result/<job_key>', methods=['GET'])
@login_required
def get_validated_result(job_key):
    job = Job.fetch(job_key, connection=get_redis_connection())
    if job.is_failed:
        logger.error(job.exc_info)
        return jsonify(format_error_report('System error. The error has been logged, please try again later'))
    if not job.is_finished:
        return jsonify({
            'validation': {
                'jobKey': job_key,
                'status': 'validating',
                'message': 'Still validating data!'
            },
            'upload_result': {
                'status': 'not yet',
            }
        })

    result = job.result
    if 'validation' in result and 'upload_result' in result:
        return jsonify(result)
    validation_report = result['validation_report']
    event_type = result['event_type']
    filename_with_all_fields = result['filename_with_all_fields']
    if validation_report['valid']:
        upload_id = job.meta['upload_id']
        row_count = validation_report['tables'][0]['row-count'] - 1

        sample_rows, field_names = get_sample(filename_with_all_fields)
        db_session.commit()
        return jsonify({
            'validation': {
                'status': 'valid',
                'jobKey': job_key,
            },
            'upload_result': {
                'status': 'done',
                'rowCount': row_count,
                'exampleRows': sample_rows,
                'fieldOrder': field_names,
                'uploadId': upload_id
            }
        })
    else:
        db_session.commit()
        return jsonify({
            'validation': {
                'jobKey': job_key,
                'status': 'invalid'
            },
            'upload_result': {
                'status': 'done',
                'rowCount': '',
                'fieldOrder': [],
                'errorReport': format_validation_report(validation_report, event_type),
                'upload_id': ''
            }
        })


def format_error_report(exception_message):
    return {
        'validation': {
            'status': 'invalid',
        },
        'upload_result': {
            'status': 'done',
            'rowCount': '',
            'fieldOrder': [],
            'errorReport': [{
                'field_name': 'unknown',
                'message': exception_message,
                'num_rows': 1,
                'values': '',
                'row_numbers': ''
            }],
            'upload_id': ''
        }
    }


def validate_async(uploaded_file_name, jurisdiction, full_filename, event_type, flask_user_id, upload_id, row_limit):
    validate_start_time = datetime.today()
    try:
        # 1. validate header
        validate_header(event_type, full_filename)
        # 2. preprocess file
        filename_with_all_fields = add_missing_fields(event_type, full_filename)

        # 3. validate body
        body_validation_report = validate_file(event_type, filename_with_all_fields, row_limit)
        sync_upload_metadata_partial = partial(
            sync_upload_metadata,
            upload_id=upload_id,
            event_type=event_type,
            jurisdiction=jurisdiction,
            flask_user_id=flask_user_id,
            given_filename=uploaded_file_name,
            local_filename=full_filename,
            db_session=db_session
        )

        validate_complete_time = datetime.today()
        if not body_validation_report['valid']:
            sync_upload_metadata_partial(
                validate_start_time=validate_start_time,
                validate_complete_time=validate_complete_time,
                validate_status=False,
            )

            return {
                'validation_report': body_validation_report,
                'event_type': event_type,
                'jurisdiction': jurisdiction,
                'filename_with_all_fields': filename_with_all_fields,
                'uploaded_file_name': uploaded_file_name,
                'full_filename': full_filename
            }

        try:
            # 4. upload to s3
            upload_start_time = datetime.today()
            upload_path = s3_upload_path(jurisdiction, event_type, upload_id)
            upload_to_s3(upload_path, filename_with_all_fields)

            # 5. load into raw table
            copy_raw_table_to_db(
                upload_path,
                event_type,
                upload_id,
                db_session.get_bind()
            )

            upload_complete_time = datetime.today()
            # 6. sync upload metadata to db
            sync_upload_metadata_partial(
                s3_upload_path=upload_path,
                validate_start_time=validate_start_time,
                validate_complete_time=validate_complete_time,
                validate_status=True,
                upload_start_time=upload_start_time,
                upload_complete_time=upload_complete_time,
                upload_status=True
            )
        except ValueError as e:
            sync_upload_metadata_partial(
                validate_start_time=validate_start_time,
                validate_complete_time=validate_complete_time,
                validate_status=False,
                upload_start_time=upload_start_time,
                upload_status=False,
            )
            body_validation_report = {
                'valid': False,
                'tables': [{
                    'headers': [] ,
                    'errors': [{
                        'column-number': None,
                        'row-number': None,
                        'message': str(e)
                    }]
                }]
            }

        db_session.commit()

        return {
            'validation_report': body_validation_report,
            'event_type': event_type,
            'jurisdiction': jurisdiction,
            'filename_with_all_fields': filename_with_all_fields,
            'uploaded_file_name': uploaded_file_name,
            'full_filename': full_filename
        }

    except ValueError as e:
        sync_upload_metadata_partial(
            validate_start_time=validate_start_time,
            validate_status=False
        )

        db_session.commit()
        return format_error_report(str(e))


@upload_api.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    jurisdiction = request.args.get('jurisdiction')
    event_type = request.args.get('eventType')
    if can_upload_file(jurisdiction, event_type):
        filenames = [key for key in request.files.keys()]
        if len(filenames) != 1:
            return jsonify(status='error', message='Exactly one file must be uploaded at a time')
        uploaded_file = request.files[filenames[0]]
        filename = secure_filename(uploaded_file.filename)
        cwd = os.getcwd()
        full_filename = os.path.join(cwd + '/tmp', filename)
        uploaded_file.save(full_filename)
        upload_id = unique_upload_id()
        q = get_q(get_redis_connection())
        job = q.enqueue_call(
            func=validate_async,
            args=(uploaded_file.filename, jurisdiction, full_filename, event_type, current_user.id, upload_id, 10000000),
            result_ttl=5000,
            timeout=3600,
            meta={'event_type': event_type, 'filename': filename, 'upload_id': upload_id}
        )
        logger.info(f"Job id {job.get_id()}")
        return jsonify(
            status='validating',
            jobKey=job.get_id(),
            message='Validating data!'
        )
    else:
        return jsonify(
            status='not authorized',
            exampleRows=[]
        )


@upload_api.route('/merge_file', methods=['POST'])
@login_required
def merge_file():
    upload_id = request.args.get('uploadId', None)
    if not upload_id:
        return jsonify(status='invalid', reason='uploadId not present')
    has_access = False
    try:
        has_access = can_access_file(upload_id)
        if has_access:
            upload_log = db_session.query(Upload).get(upload_id)
            logger.info('Retrieved upload log, merging raw table to master')
            raw_table_name = 'raw_{}'.format(upload_id)
            logger.info('Merging raw table to master')
            merge_id = upsert_raw_table_to_master(
                raw_table_name,
                upload_log.jurisdiction_slug,
                upload_log.event_type_slug,
                upload_id,
                db_session
            )
            logger.info('Syncing merged file to s3')

            bootstrap_matched_tables(
                jurisdiction=upload_log.jurisdiction_slug,
                db_session=db_session
            )

            sync_merged_file_to_s3(
                upload_log.jurisdiction_slug,
                upload_log.event_type_slug,
                db_session.get_bind()
            )
            merge_log = db_session.query(MergeLog).get(merge_id)
            try:
                logger.info('Merge succeeded. Now querying matcher')
                notify_matcher(upload_log.jurisdiction_slug, upload_id)
            except Exception as e:
                logger.error('Error matching: ', e)
                db_session.rollback()
                return make_response(jsonify(status='error'), 500)
            db_session.commit()
            return jsonify(
                status='valid',
                new_unique_rows=merge_log.new_unique_rows,
                total_unique_rows=merge_log.total_unique_rows
            )
        else:
            return jsonify(status='not authorized')
    except ValueError as e:
        logger.error('Error merging: ', e)
        db_session.rollback()
        return make_response(jsonify(status='error'), 500)
