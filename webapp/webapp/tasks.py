from smart_open import smart_open
from datetime import datetime
from goodtables import validate
from webapp.models import Upload, MergeLog
from webapp.utils import load_schema_file,\
    create_statement_from_goodtables_schema,\
    column_list_from_goodtables_schema,\
    create_statement_from_column_list,\
    generate_master_table_name,\
    merged_file_path,\
    schema_filename,\
    lower_first,\
    infer_delimiter
from webapp.validations import CHECKS_BY_SCHEMA
from hashlib import md5
import logging
import os
import unicodecsv as csv


def upload_to_s3(full_s3_path, local_filename):
    with smart_open(full_s3_path, 'wb') as outfile:
        with smart_open(local_filename, 'rb') as infile:
            outfile.write(infile.read())


def sync_upload_metadata(
    upload_id,
    event_type,
    jurisdiction,
    user,
    given_filename,
    local_filename,
    s3_upload_path,
    db_session
):
    with smart_open(local_filename, 'rb') as infile:
        num_rows = sum(1 for _ in infile)
        infile.seek(0)
        file_size = os.fstat(infile.fileno()).st_size
        file_hash = md5(infile.read()).hexdigest()

        db_object = Upload(
            id=upload_id,
            jurisdiction_slug=jurisdiction,
            event_type_slug=event_type,
            user_id=user.id,
            given_filename=given_filename,
            upload_timestamp=datetime.today(),
            num_rows=num_rows,
            file_size=file_size,
            file_hash=file_hash,
            s3_upload_path=s3_upload_path
        )
        db_session.add(db_object)
        db_session.commit()


def copy_raw_table_to_db(
    full_s3_path,
    event_type,
    upload_id,
    db_engine
):
    goodtables_schema = load_schema_file(event_type)
    logging.info('Loaded schema: %s', goodtables_schema)
    table_name = 'raw_{}'.format(upload_id)
    create_statement = create_statement_from_goodtables_schema(
        goodtables_schema,
        table_name
    )
    logging.info('Assembled create table statement: %s', create_statement)
    db_engine.execute(create_statement)
    logging.info('Successfully created table')
    with smart_open(full_s3_path, 'rb') as infile:
        cursor = db_engine.raw_connection().cursor()
        copy_stmt = 'copy "{}" from stdin with csv header delimiter as \',\''.format(table_name)
        cursor.copy_expert(copy_stmt, infile)
    logging.info('Successfully loaded file')
    return table_name


def upsert_raw_table_to_master(
    raw_table_name,
    jurisdiction,
    event_type,
    upload_id,
    db_session
):
    master_table_name = generate_master_table_name(jurisdiction, event_type)
    goodtables_schema = load_schema_file(event_type)
    base_column_list = column_list_from_goodtables_schema(goodtables_schema)
    # mutate column list
    full_column_list = base_column_list + [('inserted_ts', 'timestamp'), ('updated_ts', 'timestamp')]
    create = create_statement_from_column_list(full_column_list, master_table_name, goodtables_schema['primaryKey'])
    # create table if it does not exist
    logging.info('Assembled create-if-not-exists table statement: %s', create)
    db_session.execute(create)
    # use new postgres 'on conflict' functionality to upsert
    update_statements = [
        ' "{column}" = EXCLUDED."{column}"'.format(column=column_def[0])
        for column_def in base_column_list
    ]
    start_ts = datetime.today()
    insert_sql = '''
        insert into {master}
        select raw.*, '{new_ts}' inserted_ts, '{new_ts}' updated_ts
        from "{raw}" as raw
        on conflict ({primary_key})
        do update set {update_string}, updated_ts = '{new_ts}'
    '''.format(
        raw=raw_table_name,
        master=master_table_name,
        primary_key=', '.join(["\"{}\"".format(col) for col in goodtables_schema['primaryKey']]),
        update_string=', '.join(update_statements),
        new_ts=start_ts.isoformat()
    )
    logging.info('Executing insert: %s', insert_sql)
    db_session.execute(insert_sql)
    end_ts = datetime.today()
    merge_log = MergeLog(
        upload_id=upload_id,
        total_unique_rows=total_unique_rows(raw_table_name, goodtables_schema['primaryKey'], db_session),
        new_unique_rows=new_unique_rows(master_table_name, start_ts, db_session),
        merge_start_timestamp=start_ts,
        merge_complete_timestamp=end_ts,
    )
    db_session.add(merge_log)
    db_session.commit()
    return merge_log.id

def new_unique_rows(master_table_name, new_ts, db_session):
    return [
        row[0] for row in
        db_session.execute('''select count(*) from "{}" where inserted_ts='{}' '''.format(master_table_name, new_ts))
    ][0]


def total_unique_rows(raw_table_name, primary_key, db_engine):
    return [
        row[0] for row in
        db_engine.execute('select count(*) from "{}"'.format(
            raw_table_name
        )
    )][0]


def sync_merged_file_to_s3(jurisdiction, event_type, db_engine):
    full_s3_path = merged_file_path(jurisdiction, event_type)
    table_name = generate_master_table_name(jurisdiction, event_type)
    with smart_open(full_s3_path, 'wb') as outfile:
        cursor = db_engine.raw_connection().cursor()
        copy_stmt = 'copy "{}" to stdout with csv header delimiter as \'|\''.format(table_name)
        cursor.copy_expert(copy_stmt, outfile)




def add_missing_fields(event_type, infilename):
    goodtables_schema = load_schema_file(event_type)
    schema_fields = [field['name'] for field in goodtables_schema['fields']]
    outfilename = infilename + '.filled'
    delimiter = infer_delimiter(infilename)
    with open(infilename, 'rb' ) as infileobj, open(outfilename, 'wb') as outfileobj:
        reader = csv.DictReader(lower_first(infileobj), delimiter=delimiter)
        writer = csv.DictWriter(outfileobj, fieldnames=schema_fields)
        writer.writeheader()
        for line in reader:
            newline = {}
            for field in schema_fields:
                if field not in line:
                    newline[field] = ''
                else:
                    newline[field] = line[field]
            writer.writerow(newline)
    return outfilename


def validate_file(event_type, filename_with_all_fields, row_limit=1000):
    report = validate(
        filename_with_all_fields,
        schema=schema_filename(event_type),
        skip_checks=['required-constraint'],
        checks=CHECKS_BY_SCHEMA[event_type],
        order_fields=True,
        row_limit=row_limit,
        format='csv'
    )

    return report
