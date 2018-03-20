# coding: utf-8

import subprocess
import logging
logger = logging.getLogger('utils')

import numpy as np
import pandas as pd
from io import StringIO
import boto3
import psycopg2
import smart_open
import botocore


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


# these are the columns that, in combination, are the unique row index for each data type
# we need to be able to match back to the source data on these columns.
# i think the best way to do this may be to concatenate them as a single 
# string as a new column 'source_index' or something every time the data are loaded.
# this way. we can reconnect the matched data to all the columns in the source data
# when we go to write the data.
INDEXES = {
    'jail_bookings': ['internal_event_id', 'booking_number', 'location_date'],
    'booking_aka': ['internal_event_id', 'booking_number'],
    'booking_charges': ['internal_event_id', 'internal_charge_id', 'booking_number', 'charge_position', 'charge_date'],
    'case_charges': ['internal_event_id', 'internal_charge_id', 'case_number', 'charge_position', 'charge_date'],
    'hmis_service_stays': ['internal_event_id', 'client_location_start_date'],
    'hmis_aka': ['internal_event_id', 'project_start_date'],
    'by_name': ['internal_event_id', 'full_name', 'first_name', 'middle_name', 'last_name', 'list_entry_date']
}


def concatenate_source_index(df:pd.DataFrame, event_type:str) -> pd.Series:
    index_column_names = INDEXES[event_type]
    index_columns = df[index_column_names]
    return index_columns.apply(lambda x: ''.join(x.map(str)), axis=1)


def read_merged_data_from_s3(jurisdiction:str, event_type:str, s3_bucket:str) -> pd.DataFrame:
    # Read the data in and select the necessary columns
    logger.info(f"Reading data from {s3_bucket}/{jurisdiction}/{event_type}")
    merged_key = f'csh/matcher/{jurisdiction}/{event_type}/merged'
    df=pd.read_csv(f's3://{s3_bucket}/{merged_key}', sep='|')
 
    return df


def load_data_for_matching(jurisdiction:str, event_type:str, s3_bucket:str, keys:list) -> pd.DataFrame:
    logger.info(f'Loading {jurisdiction} {event_type} data for matching.')
    try:
        df = read_merged_data_from_s3(jurisdiction, event_type, s3_bucket)
        df['source_index'] = concatenate_source_index(df, event_type)
        df = select_columns(
            df=df,
            keys=keys,
            event_type=event_type
        )
        df['event_type'] = event_type
        logger.info(f'{jurisdiction} {event_type} data loaded from S3.')
        return df
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            logger.info(f'No merged file found for {jurisdiction} {event_type}. Skipping.')
            pass
        else:
            raise


def get_matched_table_name(jurisdiction:str, event_type:str) -> str:
    return f'{jurisdiction}_{event_type}_matched'

def write_matched_data(df:pd.DataFrame, jurisdiction:str, event_type:str, s3_bucket:str, pg_keys:dict):
    logger.info(f'Writing matched data for {jurisdiction} {event_type}')
    df = df[df.event_type == event_type]
    right_df=read_merged_data_from_s3(jurisdiction, event_type, s3_bucket)
    right_df['source_index'] = concatenate_source_index(right_df, event_type)
    cols_to_use = np.append(right_df.columns.difference(df.columns).values, 'source_index')
    df = df.merge(
        right=right_df[cols_to_use],
        on='source_index',
        copy=False,
        validate='one_to_one'
    )
    key = f'csh/matcher/{jurisdiction}/{event_type}/matched'
    write_to_s3(df, s3_bucket, key)
    logger.info(f'Written data for {jurisdiction} {event_type} to S3.')
    write_matched_data_to_postgres(
        bucket=s3_bucket, 
        key=key, 
        table_name=get_matched_table_name(jurisdiction, event_type), 
        pg_keys=pg_keys,
        column_names=df.columns.values
    )
    logger.info(f'Written data for {jurisdiction} {event_type} to postgres.')


def select_columns(df:pd.DataFrame, keys:list, event_type:str) -> pd.DataFrame:
    """ 
    Reduces the dataframe to the columns selected for matching.
    
    We always expect at least two columns: source and source_id
    """
    logger.info(f'Selecting columns for matching.')
    columns_to_select = ['source', 'source_id', 'internal_person_id', 'source_index']
    if keys:
        columns_to_select = columns_to_select + keys
    
    return df.loc[:,columns_to_select]


def read_matched_data_from_postgres(table_name:str, pg_keys:dict):
    conn = psycopg2.connect(**pg_keys)
    cur = conn.cursor()

    sql = f"SELECT * FROM matched.{table_name};"
    dat = pd.io.sql.read_sql_query(sql, conn)

    conn.close()

    return dat


def write_matched_data_to_postgres(bucket, key, table_name, pg_keys, column_names):
    conn = psycopg2.connect(**pg_keys)
    cur = conn.cursor()

    logger.info(f'Creating table matched.{table_name}')
    col_list = [f'{col} varchar' for col in column_names]
    col_type_list = ', '.join(col_list)
    create_table_query = f"""
        CREATE SCHEMA IF NOT EXISTS matched;
        DROP TABLE IF EXISTS matched.{table_name};
        CREATE TABLE matched.{table_name} (
            {col_type_list}
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
    logger.info(f'Writing data to s3://{bucket}/{key}')
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

    logger.debug("Cartesian called")

    logger.debug(f"Size of the first dataframe: {df1.shape}")
    logger.debug(f"Indexes of df1 are {df1.index}")
    logger.debug(f"Columns of df1 are {df1.columns}")
    
    #suffixes = ['_'+s for s in sources]

    if df2 is None:
        logger.debug(f"Second dataframe not specified, copying from df1")
        df2=df1.copy()

    df1['_tmpkey'] = 1
    df2['_tmpkey'] = 1

    df = pd.merge(df1, df2, on='_tmpkey', suffixes=['_left', '_right']).drop('_tmpkey', axis=1)
    df.index = pd.MultiIndex.from_product((df1.index, df2.index))
    # df1.drop("_tmpkey", axis=1, inplace=True)
    # df2.drop("_tmpkey", axis=1, inplace=True)

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
