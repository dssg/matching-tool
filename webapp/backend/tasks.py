from datetime import datetime
from goodtables import validate
from backend.database import db_session, engine
from backend.logger import logger
from backend.models import Upload, MergeLog, MatchLog
from backend.storage import open_sesame
from backend.utils import load_schema_file,\
    create_statement_from_goodtables_schema,\
    column_list_from_goodtables_schema,\
    create_statement_from_column_list,\
    generate_master_table_name,\
    master_table_column_list,\
    merged_file_path,\
    schema_filename,\
    lower_first,\
    infer_delimiter,\
    primary_key_statement,\
    table_exists,\
    table_has_column,\
    split_table,\
    generate_raw_table_name,\
    db_retry
from backend.validations import CHECKS_BY_SCHEMA
from hashlib import md5
import logging
import os
import re
import unicodecsv as csv
import psycopg2


def upload_to_storage(full_path, local_filename):
    with open_sesame(full_path, 'wb') as outfile:
        with open_sesame(local_filename, 'rb') as infile:
            outfile.write(infile.read())


@db_retry
def sync_upload_metadata(
    upload_id,
    event_type,
    jurisdiction,
    flask_user_id,
    given_filename,
    local_filename,
    db_session,
    s3_upload_path=None,
    validate_start_time=None,
    validate_complete_time=None,
    validate_status=None,
    upload_start_time=None,
    upload_complete_time=None,
    upload_status=None,
):
    with open_sesame(local_filename, 'rb') as infile:
        num_rows = sum(1 for _ in infile)
        infile.seek(0)
        file_size = os.fstat(infile.fileno()).st_size
        file_hash = md5(infile.read()).hexdigest()

        write_upload_log(
            db_session=db_session,
            upload_id=upload_id,
            jurisdiction_slug=jurisdiction,
            event_type_slug=event_type,
            user_id=flask_user_id,
            given_filename=given_filename,
            upload_start_time=upload_start_time,
            upload_complete_time=upload_complete_time,
            upload_status=upload_status,
            validate_start_time=validate_start_time,
            validate_complete_time=validate_complete_time,
            validate_status=validate_status,
            num_rows=num_rows,
            file_size=file_size,
            file_hash=file_hash,
            s3_upload_path=s3_upload_path
        )

@db_retry
def copy_raw_table_to_db(
    full_path,
    event_type,
    upload_id,
    db_engine
):
    goodtables_schema = load_schema_file(event_type)
    logging.info('Loaded schema: %s', goodtables_schema)
    table_name = generate_raw_table_name(upload_id)
    create_statement = create_statement_from_goodtables_schema(
        goodtables_schema,
        table_name
    )
    logging.info('Assembled create table statement: %s', create_statement)
    db_engine.execute(create_statement)
    logging.info('Successfully created table')
    primary_key = primary_key_statement(goodtables_schema['primaryKey'])
    with open_sesame(full_path, 'rb') as infile:
        conn = db_engine.raw_connection()
        cursor = conn.cursor()
        copy_stmt = 'copy "{}" from stdin with csv force not null {}  header delimiter as \',\' '.format(table_name, primary_key)
        try:
            cursor.copy_expert(copy_stmt, infile)
            conn.commit()
        except psycopg2.IntegrityError as e:
            error_message = str(e)
            conn.rollback()
            if 'duplicate key value violates unique constraint' not in error_message:
                raise
            error_message_lines = error_message.split('\n')
            if len(error_message_lines) < 3:
                raise
            line_no_match = re.match(r'^.*(line \d+)', error_message.split('\n')[2])
            if not line_no_match:
                raise
            line_no = line_no_match.group(1)
            raise ValueError(f"Duplicate key value found on {line_no}. {error_message_lines[1]}")
        finally:
            conn.close()
    logging.info('Successfully loaded file')
    return table_name


@db_retry
def create_merged_table(jurisdiction, event_type, db_session):
    master_table_name = generate_master_table_name(jurisdiction, event_type)
    goodtables_schema = load_schema_file(event_type)
    full_column_list = master_table_column_list(goodtables_schema)
    create = create_statement_from_column_list(full_column_list, master_table_name, goodtables_schema['primaryKey'])
    # create table if it does not exist
    logging.info('Assembled create-if-not-exists table statement: %s', create)
    db_session.execute(create)


@db_retry
def bootstrap_master_tables(jurisdiction, db_session):
    for event_type in {'hmis_service_stays', 'jail_bookings'}:
        create_merged_table(jurisdiction, event_type, db_session)


@db_retry
def upsert_raw_table_to_master(
    raw_table_name,
    jurisdiction,
    event_type,
    upload_id,
    db_session
):
    create_merged_table(jurisdiction, event_type, db_session)
    master_table_name = generate_master_table_name(jurisdiction, event_type)
    goodtables_schema = load_schema_file(event_type)
    base_column_list = column_list_from_goodtables_schema(goodtables_schema)
    # use new postgres 'on conflict' functionality to upsert
    update_statements = [
        ' "{column}" = EXCLUDED."{column}"'.format(column=column_def[0])
        for column_def in base_column_list
    ]
    start_ts = datetime.today()
    insert_sql = '''
        insert into {master}
        select raw.*, '{new_ts}' inserted_ts, '{new_ts}' updated_ts, row_number() over ()::text || '{event_type}' as matched_id
        from "{raw}" as raw
        on conflict ({primary_key})
        do update set {update_string}, updated_ts = '{new_ts}'
    '''.format(
        raw=raw_table_name,
        master=master_table_name,
        event_type=event_type,
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
    db_session.execute('drop table "{}"'.format(raw_table_name))
    db_session.commit()
    return merge_log.id


@db_retry
def new_unique_rows(master_table_name, new_ts, db_session):
    return [
        row[0] for row in
        db_session.execute('''select count(*) from "{}" where inserted_ts='{}' '''.format(master_table_name, new_ts))
    ][0]


@db_retry
def total_unique_rows(raw_table_name, primary_key, db_engine):
    return [
        row[0] for row in
        db_engine.execute('select count(*) from "{}"'.format(
            raw_table_name
        )
    )][0]


@db_retry
def sync_merged_file_to_storage(jurisdiction, event_type, db_engine):
    full_path = merged_file_path(jurisdiction, event_type)
    table_name = generate_master_table_name(jurisdiction, event_type)
    with open_sesame(full_path, 'wb') as outfile:
        cursor = db_engine.raw_connection().cursor()
        copy_stmt = 'copy "{}" to stdout with csv header delimiter as \'|\''.format(table_name)
        cursor.copy_expert(copy_stmt, outfile)


def add_missing_fields(event_type, infilename):
    goodtables_schema = load_schema_file(event_type)
    schema_fields = goodtables_schema['fields']
    outfilename = infilename + '.filled'
    delimiter = infer_delimiter(infilename)
    with open(infilename, 'rb' ) as infileobj, open(outfilename, 'wb') as outfileobj:
        reader = csv.DictReader(lower_first(infileobj), delimiter=delimiter)
        writer = csv.DictWriter(outfileobj, fieldnames=[field['name'] for field in schema_fields], quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        try:
            for line in reader:
                newline = {}
                for field in schema_fields:
                    field_name = field['name']
                    if field_name not in line or not line[field_name]:
                        if field['type'] == 'integer':
                            newline[field_name] = None
                        else:
                            newline[field_name] = ''
                    else:
                        if field['type'] == 'string':
                            newline[field_name] = line[field_name].strip()
                        else:
                            newline[field_name] = line[field_name]
                writer.writerow(newline)
        except Exception as e:
            raise ValueError('Line %s has error: %s', reader.line_num, e)
    return outfilename


def two_pass_validation(event_type, filename_with_all_fields):
    first_pass_rows = 100
    initial_report = validate_file(event_type, filename_with_all_fields, row_limit=first_pass_rows)
    if len(initial_report['tables'][0]['errors']) >= first_pass_rows:
        initial_report['tables'][0]['errors'].append({
            'column-number': None,
            'row-number': None,
            'message': f'Too many errors in first {first_pass_rows}, rest of file skipped. Please fix errors and try again.'
        })
        return initial_report
    else:
        return validate_file(event_type, filename_with_all_fields, row_limit=10000000)


def validate_file(event_type, filename_with_all_fields, row_limit=1000):
    report = validate(
        filename_with_all_fields,
        schema=schema_filename(event_type),
        skip_checks=['required-constraint'],
        checks=CHECKS_BY_SCHEMA[event_type],
        order_fields=True,
        row_limit=row_limit,
        error_limit=100000000,
        format='csv'
    )

    return report


def validate_header(event_type, filename_without_all_fields):
    goodtables_schema = load_schema_file(event_type)
    schema_fields = goodtables_schema['fields']
    delimiter = infer_delimiter(filename_without_all_fields)
    required_field_names = set(
        field['name']
        for field in schema_fields
        if field.get('constraints', {}).get('required', False)
    )
    with open(filename_without_all_fields, 'rb' ) as infileobj:
        reader = csv.DictReader(lower_first(infileobj), delimiter=delimiter)
        first_line = next(reader)
        for required_field_name in required_field_names:
            if required_field_name not in first_line:
                raise ValueError(f"Field name {required_field_name} is required for {event_type} schema but is not present")


@db_retry
def write_upload_log(
    db_session,
    upload_id,
    jurisdiction_slug,
    event_type_slug,
    user_id,
    given_filename,
    upload_start_time,
    upload_complete_time,
    upload_status,
    validate_start_time,
    validate_complete_time,
    validate_status,
    num_rows,
    file_size,
    file_hash,
    s3_upload_path
):
    db_object = Upload(
            id=upload_id,
            jurisdiction_slug=jurisdiction_slug,
            event_type_slug=event_type_slug,
            user_id=user_id,
            given_filename=given_filename,
            upload_start_time=upload_start_time,
            upload_complete_time=upload_complete_time,
            upload_status=upload_status,
            validate_start_time=validate_start_time,
            validate_complete_time=validate_complete_time,
            validate_status=validate_status,
            num_rows=num_rows,
            file_size=file_size,
            file_hash=file_hash,
            s3_upload_path=s3_upload_path
    )
    db_session.add(db_object)
    db_session.commit()


@db_retry
def write_match_log(db_session, match_job_id, upload_id, match_start_at, match_complete_at, match_status, match_runtime):
    db_object = MatchLog(
        id=match_job_id,
        upload_id=upload_id,
        match_start_timestamp=match_start_at,
        match_complete_timestamp=match_complete_at,
        match_status=match_status,
        runtime=match_runtime
    )
    db_session.add(db_object)
    db_session.commit()


@db_retry
def write_matches_to_db(db_engine, event_type, jurisdiction, matches_filehandle):
    goodtables_schema = load_schema_file(event_type)
    table_name = generate_master_table_name(event_type=event_type, jurisdiction=jurisdiction)
    logging.info('Writing matches for %s / %s to table %s', event_type, jurisdiction, table_name)
    reader = csv.reader(matches_filehandle, delimiter='|')
    ordered_column_names = next(reader)
    matches_filehandle.seek(0)

    # 1. create pseudo-temporary table for the raw matches file
    # use the CSV's column order but grab the definitions from the goodtables schema
    unordered_column_list = column_list_from_goodtables_schema(goodtables_schema)
    primary_key = goodtables_schema['primaryKey']

    all_columns = [('matched_id', 'varchar')] + [col for col in unordered_column_list if col[0] in primary_key]
    column_definitions = dict((col[0], col) for col in all_columns)
    ordered_column_list = [column_definitions[ordered_column_name] for ordered_column_name in ordered_column_names]
    logging.info('Final column list for temporary matches-only table: %s', ordered_column_list)
    create = create_statement_from_column_list(ordered_column_list, table_name, primary_key)
    temp_table_name = 'temp_matched_merge_tbl'
    create = create.replace(table_name, temp_table_name)
    logging.info(create)
    db_engine.execute(create)

    # 2. copy data from filehandle to
    conn = db_engine.raw_connection()
    cursor = conn.cursor()
    pk = ','.join([col for col in primary_key])
    copy_stmt = 'copy {} from stdin with csv header delimiter as \'|\' force not null {}'.format(temp_table_name, pk)
    try:
        logging.info(copy_stmt)
        cursor.copy_expert(copy_stmt, matches_filehandle)
        logging.info('Status message after COPY: %s', cursor.statusmessage)
        for notice in conn.notices:
            logging.info('Notice from database connection: %s', notice)
        conn.commit()
        cursor = conn.cursor()
        cursor.execute('select * from {} limit 5'.format(temp_table_name))
        logging.info('First five rows: %s', [row for row in cursor])
        big_query = """
update {matched_table} as m set matched_id = regexp_replace(tmp.matched_id::text, '[^\w]', '', 'g')
        from {temp_table_name} tmp where ({pk}) """.format(
            create=create,
            matched_table=table_name,
            temp_table_name= temp_table_name,
            pk=' and '.join(['tmp.{col} = m.{col}'.format(col=col) for col in primary_key])
        )
        logging.info('Updating matches in %s with rows from %s', table_name, temp_table_name)
        logging.info(big_query)
        cursor.execute(big_query)
        logging.info('Status message after UPDATE: %s', cursor.statusmessage)
        conn.commit()
    except Exception as e:
        logging.error('Error encountered! Rolling back merge of matched ids. Original error: %s', str(e))
        conn.rollback()
    finally:
        db_engine.execute('drop table if exists {}'.format(temp_table_name))


def match_finished(
    matched_results_paths,
    match_job_id,
    match_start_at,
    match_complete_at,
    match_status,
    match_runtime,
    upload_id=None
):
    try:
        logger.info('Writing to match log')
        write_match_log(
            db_session=db_session,
            match_job_id=match_job_id,
            match_start_at=match_start_at,
            match_complete_at=match_complete_at,
            match_status=match_status,
            match_runtime=match_runtime,
            upload_id=upload_id
        )
        logger.info('Writing matches to db')
        for event_type, filename in matched_results_paths.items():
            jurisdiction = filename.split('/')[-3]
            logger.info('Writing matches from event type %s and filename %s to db. Parsed jurisdiction %s out of filename', event_type, filename, jurisdiction)
            with open_sesame(filename, 'rb') as matches_filehandle:
                write_matches_to_db(
                    db_engine=engine,
                    event_type=event_type,
                    jurisdiction=jurisdiction,
                    matches_filehandle=matches_filehandle
                )
    except Exception as e:
        logger.error('Error encountered during match_finished: %s', str(e))

    finally:
        logger.info('All done!')
