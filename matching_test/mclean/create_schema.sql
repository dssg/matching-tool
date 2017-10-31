/* This script creates a schema for holding the raw data provided by McLean
 * County, including tables to hold bookings and homelessness data.
 */

DROP SCHEMA IF EXISTS raw CASCADE;
CREATE SCHEMA raw;

DROP TABLE IF EXISTS raw.bookings_20170923;
CREATE TABLE raw.bookings_20170923 (
    internal_person_id int,
    internal_event_id int,
    full_name text,
    dob timestamp,
    ssn varchar(9),
    dmv_number text,
    dmv_state text,
    additional_id_name text,
    additional_id_number text,
    sex char(1),
    race char(1),
    ethnicity text,
    hair_color text,
    eye_color text,
    height int,
    weight int,
    homeless boolean,
    street_address text,
    city text,
    state text,
    postal_code text,
    country text,
    birth_place text,
    booking_number text,
    jail_entry_date timestamp,
    jail_exit_date timestamp,
    arresting_agency text,
    location_type text,
    relocation_date timestamp,
    source_name text,
    created_date timestamp,
    updated_date timestamp
);
CREATE INDEX ON raw.bookings_20170923 (internal_event_id);

DROP TABLE IF EXISTS raw.path_client_data_20170906;
CREATE TABLE raw.path_client_data_20170906 (
    Active boolean,
    Alias text,
    Anonymous boolean,
    Client_ID int,
    Date_Added timestamp,
    Date_Updated timestamp,
    First_Name text,
    Last_Name text,
    Middle_Name text,
    Name_Data_Quality text,
    Provider_Creating text,
    Provider_Updating text,
    Soc_Sec_No int,
    Soc_Sec_No_Dashed text,
    Soc_Sec_No_Sorted text,
    SSN_Data_Quality text,
    Suffix text,
    Unique_ID text,
    Unnamed_Client boolean,
    User_Creating text,
    User_Updating text,
    US_Military_Veteran text
);
CREATE INDEX ON raw.path_client_data_20170906 (Client_ID);

