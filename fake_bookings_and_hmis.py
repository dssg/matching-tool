from __future__ import division

import argparse
import itertools
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


def generate_rows(datasets, rows):
    fake_datasets = []
    i = 0
    for dataset in datasets:
        try:
            length = rows[i]
        except:
            i = 0
            length = rows[i]
        i = i + 1
        if dataset == 'bookings':
            data = [fake_booking() for _ in range(0, length)]
        elif dataset == 'hmis':
            data = [fake_stay() for _ in range(0, length)]
        else:
            raise ValueError(f'Unrecognized dataset type: {dataset}')

        fake_datasets.append({'data': data, 'type': dataset})
    return fake_datasets


def generate_matches(fake_datasets, matches_within, matches_between):
    for dataset1, dataset2 in itertools.product(fake_datasets, repeat=2):
        if dataset1 == dataset2:
            num_matches = matches_within
        else:
            num_matches = matches_between
        for _ in range(0, num_matches):
            row1 = dataset1['data'][random.randint(0, (len(dataset1['data']) - 1))]
            row2 = dataset2['data'][random.randint(0, (len(dataset2['data']) - 1))]
            for i in range(3, 13):
                i1 = i2 = i
                if dataset1['type'] == 'bookings':
                    i1 = i + 1
                if dataset2['type'] == 'bookings':
                    i2 = i + 1
                row1[i1] = row2[i2]
    return fake_datasets


def write_csvs(fake_datasets):
    counters = {'bookings': 0, 'hmis': 0}
    filenames = []

    for fake_dataset in fake_datasets:
        event_type = fake_dataset['type']
        counter = counters[event_type]
        filename = f'{event_type}-fake-{counter}.csv'
        with open(filename, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            if event_type == 'bookings':
                headers = [column_name for column_name, _ in booking_fakers]
            elif event_type == 'hmis':
                headers = [column_name for column_name, _ in hmis_fakers]
            writer.writerow(headers)
            for row in fake_dataset['data']:
                writer.writerow(row)
        counters[event_type] = counter + 1
        filenames.append(filename)

    return filenames


def main(datasets, rows, matches_within, matches_between):
    fake_datasets = generate_rows(datasets, rows)
    fake_datasets = generate_matches(fake_datasets, matches_within, matches_between)
    filenames = write_csvs(fake_datasets)
    
    print(('Data faking complete! Congratulations! You are a totally cool ' 
           f'person! Your files are {filenames}'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--datasets",
        type=str,
        nargs='+',
        default=['bookings', 'hmis'],
        help="tell me what type of datasets you want to fake; values should be 'bookings' or 'hmis'"
    )
    parser.add_argument(
        "-r",
        "--rows",
        type=int,
        nargs='+',
        default=[10],
        help="pass number of rows per file; will loop through values if fewer than number of datasets"
    )
    parser.add_argument(
        "-mw",
        "--matches_within",
        type=int,
        nargs='?',
        default=5,
        help="how many rows should match within files?"
    )
    parser.add_argument(
        "-mb",
        "--matches_between",
        type=int,
        nargs='?',
        default=5,
        help="how many rows should match between files?"
    )

    args = parser.parse_args()
    main(
        args.datasets,
        args.rows,
        args.matches_within,
        args.matches_between
    )
