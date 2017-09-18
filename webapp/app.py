from flask import Flask, render_template, request, jsonify
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore, http_auth_required
from flask_login import current_user
from webapp.database import db_session
from webapp.models import User, Role
from goodtables import validate
from werkzeug.utils import secure_filename
import yaml
import logging
import unicodecsv as csv
import os

# Create app
app = Flask(__name__)
with open('flask_config.yaml') as f:
    config = yaml.load(f)
    for key, val in config.items():
        app.config[key] = val


# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                User, Role)
security = Security(app, user_datastore)

PRETTY_JURISDICTION_MAP = {
    'boone': 'Boone County',
    'saltlake': 'Salt Lake County',
    'clark': 'Clark County',
    'mclean': 'McLean County',
}

PRETTY_PROVIDER_MAP = {
    'hmis': 'HMIS',
    'jail': 'Jail',
    'other': 'Other',
}

def get_jurisdiction_roles():
    jurisdiction_roles = []
    for role in current_user.roles:
        if not role.name:
            logging.warning("User Role %s has no name", role)
            continue
        parts = role.name.split('_')
        if len(parts) != 2:
            logging.warning("User role %s does not have two parts, cannot process into jurisdiction and role", role.name)
            continue
        jurisdiction, service_provider = parts
        jurisdiction_roles.append({
            'jurisdictionSlug': jurisdiction,
            'jurisdiction': PRETTY_JURISDICTION_MAP.get(jurisdiction, jurisdiction),
            'serviceProviderSlug': service_provider,
            'serviceProvider': PRETTY_PROVIDER_MAP.GET(service_provider, service_provider)
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
        return sample_rows

def validate_file(request_file, service_provider_slug):
    report = validate(
        request_file,
        schema='{}-schema.json'.format(service_provider_slug),
        format='csv'
    )
    return report

IDENTIFIER_COLUMNS = {
    'hmis': ['Internal Person ID', 'Internal Event ID']
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
            'fieldName': headers[error['column-number']],
            'message': error['message'],
        }
        new_errors[error['row-number']]['errors'].append(error_fields)

    return [row for row in new_errors.values()]

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@login_required
def home(path):
    return render_template('index.html')

@app.route('/jurisdictional_roles.json', methods=['GET'])
@http_auth_required
def jurisdiction_roles():
    return jsonify(results=get_jurisdiction_roles())


@app.route('/upload_file', methods=['POST'])
@http_auth_required
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
            sample_rows = get_sample(full_filename)
            return jsonify(
                status='valid',
                exampleRows=sample_rows
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

if __name__ == '__main__':
    app.run()
