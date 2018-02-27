# coding: utf-8

import subprocess
import logging
logger = logging.getLogger('matcher')

import pandas as pd
from io import StringIO
import boto3
import psycopg2
import smart_open


DATA_FIELDS = {
    'hmis_service_stays': """
        internal_person_id          text,
        secondary_person_id         text,
        internal_event_id           text,
        full_name                   text,
        prefix                      text,
        first_name                  text,
        middle_name                 text,
        last_name                   text,
        suffix                      text,
        name_data_quality           text,
        dob                         date,
        dob_type                    text,
        ssn                         text,
        ssn_hash                    text,
        ssn_bigrams                 text,
        ssn_data_quality            text,
        dmv_number                  text,
        dmv_state                   text,
        additional_id_number        text,
        additional_id_name          text,
        race                        text,
        secondary_race              text,
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
        source_id                   text,
        matched_id                  int
    """,
    'jail_bookings': """
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
        jail_entry_date         timestamp,
        jail_exit_date          timestamp,
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
        relocation_date         timestamp,
        case_number             text,
        source_name             text,
        created_date            timestamp,
        updated_date            timestamp,
        inserted_ts             timestamp,
        updated_ts              timestamp,
        source_id               text,
        matched_id              int
    """
}


def read_matched_data_from_postgres(table_name, pg_keys):
    conn = psycopg2.connect(**pg_keys)
    cur = conn.cursor()

    sql = f"SELECT * FROM matched.{table_name};"
    dat = pd.io.sql.read_sql_query(sql, conn)

    conn.close()

    return dat


def write_matched_data_to_postgres(bucket, key, table_name, pg_keys):
    conn = psycopg2.connect(**pg_keys)
    cur = conn.cursor()

    logger.info(f'Creating table matched.{table_name}')
    create_table_query = f"""
        CREATE SCHEMA IF NOT EXISTS matched;
        DROP TABLE IF EXISTS matched.{table_name};
        CREATE TABLE matched.{table_name} (
            {DATA_FIELDS[table_name]}
        );
    """
    logger.warning(create_table_query)
    cur.execute(create_table_query)

    logger.info(f'Inserting data into matched.{table_name}')
    with smart_open.smart_open(f's3://{bucket}/{key}') as f:
        copy_query = f"""
            COPY matched.{table_name} FROM STDIN WITH CSV HEADER DELIMITER AS '|'
        """
        cur.copy_expert(
            sql=copy_query,
            file=f
        )
    conn.commit()
    logger.info(f'Done writing matched results to matched.{table_name}')

    cur.close()
    conn.close()


def write_to_s3(df, bucket, key):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, sep='|', index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, key).put(Body=csv_buffer.getvalue())


def get_source_id(df):
    try:
        return df['matched_id']
    except KeyError:
        pass
    try:
        return df['internal_person_id']
    except KeyError:
        pass
    try:
        return df['inmate_number']
    except:
        raise ValueError('No source id column found')


def cartesian(df1:pd.DataFrame, df2:pd.DataFrame=None) -> pd.DataFrame:
    """
    Takes two data sets and generates a new data set that contains the cartesian product of the rows.
    If only one dataset is specified, this function returns a self cross join
    """

    #suffixes = ['_'+s for s in sources]

    if df2 is None:
        df2=df1.copy()


    df1['_tmpkey'] = 1
    df2['_tmpkey'] = 1



    df = pd.merge(df1, df2, on='_tmpkey', suffixes=['_left', '_right']).drop('_tmpkey', axis=1)
    df.index = pd.MultiIndex.from_product((df1.index, df2.index))
    df1.drop("_tmpkey", axis=1, inplace=True)
    df2.drop("_tmpkey", axis=1, inplace=True)

    return df


def generate_row_ids(df:pd.DataFrame) -> pd.DataFrame:
    df['row_id'] = range(0, len(df))

    return df


def version(df:pd.DataFrame) -> pd.DataFrame:
    """
    Adds the code version (git head hash) to the passed DataFrame.
    """
    # head_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).rstrip()
    df['code_version'] = '0.1' #head_hash

    return df
