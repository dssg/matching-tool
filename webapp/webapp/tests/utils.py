from webapp import app
from webapp.app import security
from webapp.models import User, Role
from webapp.database import Base, db_session
from webapp.utils import create_statement_from_goodtables_schema, load_schema_file, generate_master_table_name, master_table_column_list, create_statement_from_column_list
from sqlalchemy import create_engine
import contextlib
import testing.postgresql
from unittest.mock import patch
from moto import mock_s3
import s3fs

from flask_security import SQLAlchemySessionUserDatastore
from flask_security.utils import encrypt_password

import json
import pandas as pd

from fakeredis import FakeStrictRedis
from rq import Queue


DATA_FIELDS = {
    'hmis_service_stays': """
        internal_person_id          text,
        internal_event_id           text,
        full_name                   text,
        prefix                      text,
        first_name                  text,
        middle_name                 text,
        last_name                   text,
        suffix                      text,
        name_data_quality           text,
        dob                         date,
        ssn                         text,
        ssn_hash                    text,
        ssn_bigrams                 text,
        dmv_number                  text,
        dmv_state                   text,
        additional_id_number        text,
        additional_id_name          text,
        race                        text,
        ethnicity                   text,
        sex                         text,
        street_address              text,
        city                        text,
        state                       text,
        postal_code                 text,
        county                      text,
        country                     text,
        address_data_quality        text,
        veteran_status              text,
        disabling_condition         text,
        project_start_date          timestamp,
        project_exit_date           timestamp,
        program_name                text,
        program_type                text,
        federal_program             text,
        destination                 text,
        household_id                text,
        household_relationship      text,
        move_in_date                timestamp,
        living_situation_type       text,
        living_situation_length     text,
        living_situation_start_date timestamp,
        times_on_street             text,
        months_homeless             text,
        client_location_start_date  timestamp,
        client_location_end_date    timestamp,
        client_location             text,
        source_name                 text,
        created_date                timestamp,
        updated_date                timestamp,
        inserted_ts                 timestamp,
        updated_ts                  timestamp,
        matched_id                  text
    """,
    'jail_bookings': """
        matched_id              text,
        internal_person_id      text,
        internal_event_id       text,
        inmate_number           text,
        full_name               text,
        prefix                  text,
        first_name              text,
        middle_name             text,
        last_name               text,
        suffix                  text,
        dob                     date,
        ssn                     text,
        ssn_hash                text,
        ssn_bigrams             text,
        fingerprint_id          text,
        dmv_number              text,
        dmv_state               text,
        additional_id_number    text,
        additional_id_name      text,
        race                    text,
        ethnicity               text,
        sex                     text,
        hair_color              text,
        eye_color               text,
        height                  int,
        weight                  int,
        street_address          text,
        city                    text,
        state                   text,
        postal_code             text,
        county                  text,
        country                 text,
        birth_place             text,
        booking_number          text,
        jail_entry_date         text,
        jail_exit_date          text,
        homeless                text,
        mental_health           text,
        veteran                 text,
        special_initiative      text,
        bond_amount             text,
        arresting_agency        text,
        bed                     text,
        cell                    text,
        block                   text,
        building                text,
        annex                   text,
        floor                   text,
        classification          text,
        detention               text,
        location_type           text,
        location_date           timestamp,
        case_number             text,
        source_name             text,
        created_date            timestamp,
        updated_date            timestamp,
        inserted_ts             timestamp,
        updated_ts              timestamp
    """
}
SAMPLE_CONFIG = {
    'raw_uploads_path': 's3://test-bucket/{jurisdiction}/{event_type}/uploaded/{date}/{upload_id}',
    'merged_uploads_path': 's3://test-bucket/{jurisdiction}/{event_type}/merged'
}


def load_json_example(route):
    with open(route) as f:
        return json.load(f)


@contextlib.contextmanager
def rig_test_client():
    with testing.postgresql.Postgresql() as postgresql:
        with app.app_context():
            dburl = postgresql.url()
            engine = create_engine(dburl)
            Base.metadata.create_all(engine)
            db_session.bind = engine
            user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                            User, Role)
            app.config['SQLALCHEMY_DATABASE_URI'] = dburl
            app.config['WTF_CSRF_ENABLED'] = False
            init_app_with_options(user_datastore)
            yield app.test_client(), engine


@contextlib.contextmanager
def full_rig_with_s3():
    with full_rig_without_s3() as (app, engine):
        with mock_s3():
            s3 = s3fs.S3FileSystem()
            s3.touch('test-bucket')
            yield app, engine


@contextlib.contextmanager
def full_rig_without_s3():
    fake_redis_connection = FakeStrictRedis()
    queue = Queue(async=False, connection=fake_redis_connection)
    with patch('webapp.apis.upload.notify_matcher', return_value=None):
        with patch('webapp.apis.upload.get_redis_connection', return_value=fake_redis_connection):
            with patch('webapp.apis.upload.get_q', return_value=queue):
                with patch.dict('webapp.utils.app_config', SAMPLE_CONFIG):
                    with rig_test_client() as (app, engine):
                        authenticate(app)
                        yield app, engine


def authenticate(
        client,
        email="boone_hmis@example.com",
        password="password",
        endpoint=None,
        **kwargs):
    data = dict(email=email, password=password, remember='y')
    return client.post(endpoint or '/login', data=data, **kwargs)


def logout(client, endpoint=None, **kwargs):
    return client.get(endpoint or '/logout', **kwargs)


def create_roles(ds):
    for role in ('boone_hmis_service_stays', 'boone_jail_bookings', 'clark_hmis_service_stays', 'clark_jail_bookings'):
        ds.create_role(name=role)
    ds.commit()


def create_users(ds):
    users = [
        ('boone_hmis@example.com', 'boone hmis', 'password', ['boone_hmis_service_stays', 'boone_jail_bookings'], True),
        ('boone_jail@example.com', 'boone jail', 'password', ['boone_jail_bookings'], True),
        ('clark_hmis@example.com', 'clark hmis', 'password', ['clark_hmis_service_stays'], True),
        ('clark_jail@example.com', 'clark jail', 'password', ['clark_jail_bookings'], True),
    ]
    count = len(users)

    for u in users[:count]:
        pw = u[2]
        if pw is not None:
            pw = encrypt_password(pw)
        roles = [ds.find_or_create_role(rn) for rn in u[3]]
        ds.commit()
        user = ds.create_user(
            email=u[0],
            username=u[1],
            password=pw,
            active=u[4])
        ds.commit()
        for role in roles:
            ds.add_role_to_user(user, role)
        ds.commit()


def populate_data(user_datastore):
    create_roles(user_datastore)
    create_users(user_datastore)

def init_app_with_options(datastore, **options):
    security.datastore = datastore
    populate_data(datastore)

def create_and_populate_master_table(table_name, db_engine, file_path=None):
    full_table_name = generate_master_table_name('boone', table_name)
    create_table_query = f"""
        DROP TABLE IF EXISTS {full_table_name};
        CREATE TABLE {full_table_name} ({DATA_FIELDS[table_name]})"""
    db_engine.execute(create_table_query)
    if file_path:
        df = pd.read_csv(file_path)
        df['internal_event_id'] = df['internal_event_id'].apply(str)
        df['matched_id'] = df['matched_id'].apply(str)
        if table_name == "jail_bookings":
            df['booking_number'] = df['booking_number'].apply(lambda x: str(x) if x else None)
            df['jail_entry_date'] = pd.to_datetime(df['jail_entry_date'])
            df['jail_exit_date'] = pd.to_datetime(df['jail_exit_date'])
            df.to_sql(full_table_name, db_engine, if_exists='append', index=False)
            db_engine.execute("update {} set booking_number = null where booking_number = 'nan'".format(full_table_name))
        elif table_name == "hmis_service_stays":
            df['client_location_start_date'] = pd.to_datetime(df['client_location_start_date'])
            df['client_location_end_date'] = pd.to_datetime(df['client_location_end_date'])
            df.to_sql(full_table_name, db_engine, if_exists='append', index=False)

def create_and_populate_raw_table(raw_table, data, db_engine):
    schema = load_schema_file('test')
    n_fields = len(schema['fields'])
    for row in data:
        assert len(row) == n_fields, "sample raw data must have same # of fields as test schema"
    placeholder_string = ', '.join(['%s'] * n_fields)

    create = create_statement_from_goodtables_schema(schema, raw_table)
    db_engine.execute(create)
    for row in data:
        db_engine.execute('insert into "{}" values ({})'.format(raw_table, placeholder_string), *row)
    db_engine.execute('insert into upload_log (id, jurisdiction_slug, event_type_slug) values (%s, %s, %s)', raw_table, 'test', 'test')


def create_and_populate_merged_table(table_name, data, db_engine):
    schema = load_schema_file('test')
    n_fields = len(schema['fields'])
    for row in data:
        assert len(row) == n_fields, "sample merged data must have same # of fields as test schema"
    placeholder_string = ', '.join(['%s'] * n_fields)
    master_table_name = generate_master_table_name('test', 'test')
    column_list = master_table_column_list(schema)
    create = create_statement_from_column_list(column_list)
    db_engine.execute(create)
    for row in data:
        db_engine.execute('insert into "{}" values ({}, now(), now())'.format(master_table_name, placeholder_string), *row)
