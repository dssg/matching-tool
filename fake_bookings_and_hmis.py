from __future__ import division

import random
import csv
from functools import partial
from faker import Faker
from datetime import datetime

fake = Faker()

booking_fakers = [
    ('internal_person_id', lambda: str(random.randint(0, 10000000))),
    ('internal_event_id', lambda: str(random.randint(0, 100000000))),
    ('inmate_number', lambda: str(random.randint(0, 10000000))),
    ('full_name', lambda: ''),
    ('prefix', lambda: ''),
    ('first_name', fake.first_name),
    ('middle_name', lambda: ''),
    ('last_name', fake.last_name),
    ('suffix', lambda: ''),
    ('dob', partial(fake.date_time_between, start_date='-75y', end_date='-18y')),
    ('ssn', fake.ssn),
    ('ssn_hash', lambda: ''),
    ('ssn_bigrams', lambda: ''),
    ('fingerprint_id', lambda: str(random.randint(0, 1000000))),
    ('dmv_number', lambda: str(random.randint(0, 1000000))),
    ('dmv_state', lambda: 'FL'),
    ('additional_id_number', lambda: ''),
    ('additional_id_name', lambda: ''),
    ('race', lambda: random.choice(['white', 'black', 'amindian', 'asian', 'pacisland', 'other'])),
    ('ethnicity', lambda: random.choice(['hispanic', 'nonhispanic'])),
    ('sex', lambda: 'F'),
    ('hair_color', lambda: ''),
    ('eye_color', lambda: ''),
    ('height', lambda: None),
    ('weight', lambda: None),
    ('street_address', lambda: ''),
    ('city', lambda: ''),
    ('state', lambda: ''),
    ('postal_code', lambda: ''),
    ('county', lambda: ''),
    ('country', lambda: ''),
    ('birth_place', lambda: ''),
    ('booking_number', lambda: ''),
    ('jail_entry_date', partial(fake.date_time_between, start_date='-1y', end_date='-90d')),
    ('jail_exit_date', partial(fake.date_time_between, start_date='-90d', end_date='-1d')),
    ('homeless', lambda: ''),
    ('mental_health', lambda: ''),
    ('veteran', lambda: ''),
    ('special_initiative', lambda: ''),
    ('bond_amount', lambda: ''),
    ('arresting_agency', lambda: ''),
    ('bed', lambda: ''),
    ('cell', lambda: ''),
    ('block', lambda: ''),
    ('building', lambda: ''),
    ('annex', lambda: ''),
    ('floor', lambda: ''),
    ('classification', lambda: ''),
    ('detention', lambda: ''),
    ('location_type', lambda: ''),
    ('relocation_date', lambda: ''),
    ('case_number', lambda: ''),
    ('source_name', lambda: ''),
    ('created_date', lambda: datetime.today()),
    ('updated_date', lambda: datetime.today()),
]

hmis_fakers = [
    ('internal_person_id', lambda: str(random.randint(0, 10000000))),
    ('internal_event_id', lambda: str(random.randint(0, 100000000))),
    ('full_name', lambda: ''),
    ('prefix', lambda: ''),
    ('first_name', fake.first_name),
    ('middle_name', lambda: ''),
    ('last_name', fake.last_name),
    ('suffix', lambda: ''),
    ('name_data_quality', lambda: ''),
    ('dob', partial(fake.date_time_between, start_date='-75y', end_date='-18y')),
    ('ssn', fake.ssn),
    ('ssn_hash', lambda: ''),
    ('ssn_bigrams', lambda: ''),
    ('dmv_number', lambda: str(random.randint(0, 1000000))),
    ('dmv_state', lambda: 'FL'),
    ('additional_id_number', lambda: ''),
    ('additional_id_name', lambda: ''),
    ('race', lambda: random.choice(['white', 'black', 'amindian', 'asian', 'pacisland', 'other'])),
    ('ethnicity', lambda: random.choice(['hispanic', 'nonhispanic'])),
    ('sex', lambda: 'F'),
    ('street_address', lambda: ''),
    ('city', lambda: ''),
    ('state', lambda: ''),
    ('postal_code', lambda: ''),
    ('county', lambda: ''),
    ('country', lambda: ''),
    ('address_data_quality', lambda: ''),
    ('veteran_status', lambda: 'False'),
    ('disabling_condition', lambda: 'False'),
    ('project_start_date', partial(fake.date_time_between, start_date='-1y', end_date='-90d')),
    ('project_exit_date', partial(fake.date_time_between, start_date='-90d', end_date='-1d')),
    ('program_name', lambda: 'SAFE HAVEN SHELTER'),
    ('program_type', lambda: 'EMERGENCY SHELTER'),
    ('federal_program', lambda: 'RHSP'),
    ('destination', lambda: 8),
    ('household_id', lambda: str(random.randint(0, 100000))),
    ('household_relationship', lambda: 1),
    ('move_in_date', fake.date_this_month),
    ('living_situation_type', lambda: 'CLIENT DOESNT NOW'),
    ('living_situation_length', lambda: '90 DAYS OR MORE, BUT LESS THAN ONE YEAR'),
    ('living_situation_start_date', partial(fake.date_time_between, start_date='-4y', end_date='-2y')),
    ('times_on_street', lambda: 'THREE TIMES'),
    ('months_homeless', lambda: 32),
    ('client_location_start_date', partial(fake.date_time_between, start_date='-1y', end_date='-90d')),
    ('client_location_end_date', partial(fake.date_time_between, start_date='-90d', end_date='-1d')),
    ('client_location', lambda: 'LOCATION'),
    ('source_name', lambda: 'HOMELESS ALLIANCE OF DOVE COUNTY'),
    ('created_date', lambda: datetime.today()),
    ('updated_date', lambda: datetime.today()),
]


def fake_booking():
    return [fake_func() for _, fake_func in booking_fakers]


def fake_stay():
    return [fake_func() for _, fake_func in hmis_fakers]


def main():
    bookings = [fake_booking() for _ in range(0, 100)]
    homeless_stays = [fake_stay() for _ in range(0, 150)]

    num_matches = 10
    for _ in range(0, num_matches):
        booking = bookings[random.randint(0, 100)]
        stay = homeless_stays[random.randint(0, 150)]
        booking[3] = stay[2]
        booking[4] = stay[3]
        booking[5] = stay[4]
        booking[6] = stay[5]

    with open('bookings-fake.csv', 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        headers = [column_name for column_name, _ in booking_fakers]
        writer.writerow(headers)
        for booking in bookings:
            writer.writerow(booking)

    with open('stays-fake.csv', 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        headers = [column_name for column_name, _ in hmis_fakers]
        writer.writerow(headers)
        for stay in homeless_stays:
            writer.writerow(stay)

if __name__ == '__main__':
    main()
