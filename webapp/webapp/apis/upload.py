from flask import render_template, make_response, request, jsonify, Blueprint
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from flask_login import current_user


from webapp import app
from webapp.database import db_session
from webapp.models import User, Role, Upload, MergeLog
from webapp.tasks import \
    upload_to_s3,\
    sync_upload_metadata,\
    copy_raw_table_to_db,\
    upsert_raw_table_to_master,\
    sync_merged_file_to_s3,\
    add_missing_fields,\
    validate_file
from webapp.utils import unique_upload_id, s3_upload_path, schema_filename, notify_matcher, infer_delimiter, load_schema_file

from webapp.apis import query

from werkzeug.utils import secure_filename

from redis import Redis
from rq import Queue
from rq.job import Job
from rq.registry import StartedJobRegistry

from collections import defaultdict
import re
import requests
import yaml
import logging
import unicodecsv as csv
import boto
import os
from io import BytesIO

upload_api = Blueprint('upload_api', __name__, url_prefix='/api/upload')


PRETTY_JURISDICTION_MAP = {
    'boone': 'Boone County',
    'saltlake': 'Salt Lake County',
    'clark': 'Clark County',
    'mclean': 'McLean County',
    'test': 'Test County',
}

def get_q(redis_connection):
    return Queue('webapp', connection=redis_connection)

def get_redis_connection():
    return Redis(host='redis', port=6379)

def get_jurisdiction_roles():
    jurisdiction_roles = []
    for role in current_user.roles:
        if not role.name:
            logging.warning("User Role %s has no name", role)
            continue
        parts = role.name.split('_', maxsplit=1)
        if len(parts) != 2:
            logging.warning(
                "User role %s does not have two parts,"
                "cannot process into jurisdiction and event type",
                role.name
            )
            continue
        jurisdiction, event_type = parts
        try:
            schema_file = load_schema_file(event_type)
        except FileNotFoundError:
            logging.warning('User belongs to event_type %s that has no schema file', event_type)
            continue
        jurisdiction_roles.append({
            'jurisdictionSlug': jurisdiction,
            'jurisdiction': PRETTY_JURISDICTION_MAP.get(jurisdiction, jurisdiction),
            'eventTypeSlug': event_type,
            'eventType': schema_file.get('name')
        })
    return jurisdiction_roles


def can_upload_file(file_jurisdiction, file_event_type):
    return any(
        role['jurisdictionSlug'] == file_jurisdiction and role['eventTypeSlug'] == file_event_type
        for role in get_jurisdiction_roles()
    )


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
    logging.info(
        'Found jurisdiction %s and event type %s for upload id %s',
        upload.jurisdiction_slug,
        upload.event_type_slug,
        upload_id
    )
    return can_upload_file(upload.jurisdiction_slug, upload.event_type_slug)


def format_error_report(report, event_type_slug):
    error_summary = defaultdict(dict)
    headers = report['tables'][0]['headers']
    for error in report['tables'][0]['errors']:
        message = re.sub('row \d+ and', '', error['message'])
        message = re.sub('Row number \d+: ', '', message)
        match = re.search('The value (.*) in  column \d+', message)
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
    if job.is_finished:
        result = job.result
        if 'validation' in result and 'upload_result' in result:
            return jsonify(result)
        validation_report = result['validation_report']
        jurisdiction = result['jurisdiction']
        event_type = result['event_type']
        filename_with_all_fields = result['filename_with_all_fields']
        uploaded_file_name = result['uploaded_file_name']
        full_filename = result['full_filename']
        if validation_report['valid']:
            upload_id = unique_upload_id()
            row_count = validation_report['tables'][0]['row-count'] - 1
            upload_path = s3_upload_path(jurisdiction, event_type, upload_id)
            try:
                app.logger.info('Uploading upload_id: %s to s3', upload_id)
                upload_to_s3(upload_path, filename_with_all_fields)
            except boto.exception.S3ResponseError as e:
                logging.error(
                    'Upload id %s failed to upload to s3: %s/%s/%s. Exception: %s',
                    upload_id,
                    event_type,
                    jurisdiction,
                    uploaded_file_name,
                    e.message
                )
                db_session.commit()
                return jsonify({
                    'validation': {
                        'status': 'valid',
                        'jobKey': job_key
                    },
                    'upload_result': {
                        'status': 'error',
                        'uploadId': upload_id,
                        'message': 'Upload error!'
                    }
                })

            sync_upload_metadata(
                upload_id=upload_id,
                event_type=event_type,
                jurisdiction=jurisdiction,
                user=current_user,
                given_filename=uploaded_file_name,
                local_filename=full_filename,
                db_session=db_session,
                s3_upload_path=upload_path,
            )
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
                    'errorReport': format_error_report(validation_report, event_type),
                    'upload_id': ''
                }
            })
    else:
        db_session.commit()
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


def validate_async(uploaded_file_name, jurisdiction, full_filename, event_type, row_limit):
    try:
        filename_with_all_fields = add_missing_fields(event_type, full_filename)
    except ValueError as e:
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
                'message': str(e),
                'num_rows': 1,
                'values':'',
                'row_numbers': ''
            }],
            'upload_id': ''
        }
    }
    validation_report = validate_file(event_type, filename_with_all_fields, row_limit)
    return {
        'validation_report': validation_report,
        'event_type': event_type,
        'jurisdiction': jurisdiction,
        'filename_with_all_fields': filename_with_all_fields,
        'uploaded_file_name': uploaded_file_name,
        'full_filename': full_filename
    }


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
        q = get_q(get_redis_connection())
        job = q.enqueue_call(
            func=validate_async,
            args=(uploaded_file.filename, jurisdiction, full_filename, event_type, 1000000),
            result_ttl=5000,
            timeout=3600,
            meta={'event_type': event_type, 'filename': filename}
        )
        app.logger.info(f"Job id {job.get_id()}")
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
            logging.info('Retrieved upload log, now copying raw table')
            raw_table_name = copy_raw_table_to_db(
                upload_log.s3_upload_path,
                upload_log.event_type_slug,
                upload_id,
                db_session.get_bind()
            )
            db_session.commit()
            logging.info('Merging raw table to master')
            merge_id = upsert_raw_table_to_master(
                raw_table_name,
                upload_log.jurisdiction_slug,
                upload_log.event_type_slug,
                upload_id,
                db_session
            )
            logging.info('Syncing merged file to s3')
            sync_merged_file_to_s3(
                upload_log.jurisdiction_slug,
                upload_log.event_type_slug,
                db_session.get_bind()
            )
            merge_log = db_session.query(MergeLog).get(merge_id)
            try:
                logging.info('Merge succeeded. Now querying matcher')
                notify_matcher(upload_log.jurisdiction_slug, upload_log.event_type_slug, upload_id, upload_log.given_filename)
            except Exception as e:
                logging.error('Error matching: ', e)
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
        logging.error('Error merging: ', e)
        db_session.rollback()
        return make_response(jsonify(status='error'), 500)

