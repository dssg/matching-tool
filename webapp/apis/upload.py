from flask import render_template, request, jsonify, Blueprint
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from flask_login import current_user
from webapp.database import db_session
from webapp.models import User, Role, Upload, MergeLog
from webapp.tasks import \
    upload_to_s3,\
    sync_upload_metadata,\
    copy_raw_table_to_db,\
    upsert_raw_table_to_master,\
    sync_merged_file_to_s3
from webapp.utils import unique_upload_id, s3_upload_path
from goodtables import validate
from werkzeug.utils import secure_filename
import yaml
import logging
import unicodecsv as csv
import boto
import os

upload_api = Blueprint('upload_api', __name__, url_prefix='/api/upload')


PRETTY_JURISDICTION_MAP = {
    'boone': 'Boone County',
    'saltlake': 'Salt Lake County',
    'clark': 'Clark County',
    'mclean': 'McLean County',
    'test': 'Test County',
}

PRETTY_PROVIDER_MAP = {
    'hmis_service_stays': 'HMIS Service Stays',
    'jail_bookings': 'Jail Bookings',
    'other': 'Other',
}

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
                "cannot process into jurisdiction and service provider",
                role.name
            )
            continue
        jurisdiction, service_provider = parts
        jurisdiction_roles.append({
            'jurisdictionSlug': jurisdiction,
            'jurisdiction': PRETTY_JURISDICTION_MAP.get(jurisdiction, jurisdiction),
            'serviceProviderSlug': service_provider,
            'serviceProvider': PRETTY_PROVIDER_MAP.get(service_provider, service_provider)
        })
    return jurisdiction_roles


def can_upload_file(file_jurisdiction, file_service_provider):
    return any(
        role['jurisdictionSlug'] == file_jurisdiction and role['serviceProviderSlug'] == file_service_provider
        for role in get_jurisdiction_roles()
    )


def get_sample(saved_filename):
    with open(saved_filename, 'rb') as request_file:
        reader = csv.DictReader(request_file)
        sample_rows = []
        for x in range(10):
            try:
                sample_rows.append(next(reader))
            except StopIteration:
                break
        return sample_rows, reader.fieldnames


def validate_file(request_file, service_provider_slug):
    report = validate(
        request_file,
        schema='{}-schema.json'.format(service_provider_slug.replace('_', '-')),
        format='csv'
    )
    return report


def can_access_file(upload_id):
    upload = db_session.query(Upload).get(upload_id)
    if not upload:
        raise ValueError(
            'upload_id: %s not present in metadata database',
            upload_id
        )
    logging.info(
        'Found jurisdiction %s and service provider %s for upload id %s',
        upload.jurisdiction_slug,
        upload.service_provider_slug,
        upload_id
    )
    return can_upload_file(upload.jurisdiction_slug, upload.service_provider_slug)


IDENTIFIER_COLUMNS = {
    'hmis_service_stays': ['internal_person_id', 'internal_event_id'],
    'jail_bookings': ['internal_person_id', 'internal_event_id'],
}


def format_error_report(report, service_provider_slug):
    new_errors = {}
    headers = report['tables'][0]['headers']
    for error in report['tables'][0]['errors']:
        formatted_error = {
            'idFields': {
                'rowNumber': error['row-number'],
            },
            'errors': [],
        }
        for identifier_column in IDENTIFIER_COLUMNS[service_provider_slug]:
            identifier_index = headers.index(identifier_column)
            formatted_error['idFields'][identifier_column] = error['row'][identifier_index]
        if error['row-number'] not in new_errors:
            new_errors[error['row-number']] = formatted_error
        error_fields = {
            'fieldName': headers[error['column-number'] - 1],
            'message': error['message'],
        }
        new_errors[error['row-number']]['errors'].append(error_fields)

    return [row for row in new_errors.values()]


@upload_api.route('/jurisdictional_roles.json', methods=['GET'])
@login_required
def jurisdiction_roles():
    return jsonify(results=get_jurisdiction_roles())

@upload_api.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    jurisdiction = request.args.get('jurisdiction')
    service_provider = request.args.get('serviceProvider')
    if can_upload_file(jurisdiction, service_provider):
        filenames = [key for key in request.files.keys()]
        assert len(filenames) == 1
        uploaded_file = request.files[filenames[0]]
        filename = secure_filename(uploaded_file.filename)
        full_filename = os.path.join('/tmp', filename)
        uploaded_file.save(full_filename)
        validation_report = validate_file(full_filename, service_provider)
        if validation_report['valid']:
            upload_id = unique_upload_id()
            row_count = validation_report['tables'][0]['row-count']
            upload_path = s3_upload_path(jurisdiction, service_provider, upload_id)
            try:
                upload_to_s3(upload_path, full_filename)
            except boto.exception.S3ResponseError as e:
                logging.error(
                    'Upload id %s failed to upload to s3: %s/%s/%s',
                    upload_id,
                    service_provider,
                    jurisdiction,
                    uploaded_file.filename
                )
                return jsonify(
                    status='error',
                )

            sync_upload_metadata(
                upload_id=upload_id,
                service_provider=service_provider,
                jurisdiction=jurisdiction,
                user=current_user,
                given_filename=uploaded_file.filename,
                local_filename=full_filename,
                db_session=db_session,
                s3_upload_path=upload_path,
            )

            sample_rows, field_names = get_sample(full_filename)
            return jsonify(
                status='valid',
                rowCount=row_count,
                exampleRows=sample_rows,
                fieldOrder=field_names,
                uploadId=upload_id
            )
        else:
            return jsonify(
                status='invalid',
                exampleRows=format_error_report(validation_report, service_provider)
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
            raw_table_name = copy_raw_table_to_db(
                upload_log.s3_upload_path,
                upload_log.service_provider_slug,
                upload_id,
                db_session.get_bind()
            )
            db_session.commit()
            merge_id = upsert_raw_table_to_master(
                raw_table_name,
                upload_log.jurisdiction_slug,
                upload_log.service_provider_slug,
                upload_id,
                db_session
            )
            sync_merged_file_to_s3(
                upload_log.jurisdiction_slug,
                upload_log.service_provider_slug,
                db_session.get_bind()
            )
            merge_log = db_session.query(MergeLog).get(merge_id)
            return jsonify(
                status='valid',
                new_unique_rows=merge_log.new_unique_rows,
                total_unique_rows=merge_log.total_unique_rows
            )
        else:
            return jsonify(status='not authorized')
    except ValueError as e:
            return jsonify(status='invalid', reason=e.msg)
