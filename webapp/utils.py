from uuid import uuid4

import csv
import json
import tempfile
from datetime import date
from webapp.config import config as path_config
from webapp import SCHEMA_DIRECTORY

from contextlib import contextmanager


def unique_upload_id():
    return str(uuid4())


def s3_upload_path(jurisdiction, service_provider, upload_id):
    datestring = date.today().isoformat()
    path_template = path_config['raw_uploads_path']

    full_s3_path = path_template.format(
        service_provider=service_provider,
        jurisdiction=jurisdiction,
        date=datestring,
        upload_id=upload_id
    )
    return full_s3_path


def merged_file_path(jurisdiction, service_provider):
    path_template = path_config['merged_uploads_path']
    full_s3_path = path_template.format(
        service_provider=service_provider,
        jurisdiction=jurisdiction
    )
    return full_s3_path


@contextmanager
def makeNamedTemporaryCSV(content, separator='|'):
    tf = tempfile.NamedTemporaryFile(delete=False)
    with open(tf.name, 'w') as write_stream:
        writer = csv.writer(write_stream, delimiter=separator)
        for row in content:
            writer.writerow(row)

    yield tf.name

    tf.close()


def schema_filename(service_provider):
    return'{}/{}.json'.format(
        SCHEMA_DIRECTORY,
        service_provider.replace('_', '-')
    )


def load_schema_file(service_provider):
    with open(schema_filename(service_provider)) as f:
        return json.load(f)


def column_list_from_goodtables_schema(goodtables_schema):
    fields = goodtables_schema['fields']

    def type_map(gt_type):
        if gt_type == 'string':
            return 'varchar'
        if gt_type == 'datetime':
            return 'timestamp'
        else:
            return gt_type

    return [
        (field['name'], type_map(field['type']))
        for field in fields
    ]


def create_statement_from_column_list(column_list, table_name, primary_key):
    column_string = ', '.join(['"{}" {}'.format(column_name, column_type) for column_name, column_type in column_list])
    return 'create table if not exists "{table_name}" ({column_string}, primary key ("{primary_key}"))'.format(
        table_name=table_name,
        column_string=column_string,
        primary_key=primary_key
    )


def create_statement_from_goodtables_schema(goodtables_schema, table_name):
    column_list = column_list_from_goodtables_schema(goodtables_schema)
    primary_key = goodtables_schema['primaryKey']
    return create_statement_from_column_list(column_list, table_name, primary_key)


def generate_master_table_name(jurisdiction, service_provider):
    return '{jurisdiction}_{service_provider}_master'.format(**locals())
