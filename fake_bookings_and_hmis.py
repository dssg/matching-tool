from __future__ import division

import argparse
import itertools
import random
import csv
from functools import partial
from faker import Faker
from datetime import datetime

fake = Faker()

flags = ['N'] * 5
flags.append('Y')

# dictionaries of fields to match values on
MATCH_FIELD_INDICES = [
    {'bookings': 3, 'hmis': 2},    # full_name
    {'bookings': 4, 'hmis': 3},    # prefix
    {'bookings': 5, 'hmis': 4},    # first_name
    {'bookings': 6, 'hmis': 5},    # middle_name
    {'bookings': 7, 'hmis': 6},    # last_name
    {'bookings': 8, 'hmis': 7},    # suffix
    {'bookings': 9, 'hmis': 9},    # dob
    {'bookings': 10, 'hmis': 10},  # ssn
    {'bookings': 11, 'hmis': 11},  # ssn_hash
    {'bookings': 12, 'hmis': 12},  # ssn_bigrams
]

DATE_FIELD_INDICES = {
    'bookings': {
        'start_date': 33,
        'end_date': 34
    },
    'hmis': {
        'start_date': 43,
        'end_date': 44
    }
}

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
    ('homeless', lambda: random.choice(flags)),
    ('mental_health', lambda: random.choice(flags)),
    ('veteran', lambda: random.choice(flags)),
    ('special_initiative', lambda: random.choice(flags)),
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
    ('veteran_status', lambda: random.choice(flags)),
    ('disabling_condition', lambda: random.choice(flags)),
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
        # how many rows in this data set? loop through the list of lengths
        try:
            length = rows[i]
        except:
            i = 0
            length = rows[i]
        i = i + 1

        # generate as many rows of the right type as the length
        if dataset == 'bookings':
            data = [fake_booking() for _ in range(0, length)]
        elif dataset == 'hmis':
            data = [fake_stay() for _ in range(0, length)]
        else:
            raise ValueError(f'Unrecognized dataset type: {dataset}')

        # sort the dataset by start date
        data.sort(key=lambda x: x[DATE_FIELD_INDICES[dataset]['start_date']])

        fake_datasets.append({'data': data, 'type': dataset})

    return fake_datasets


def apply_matches(fake_datasets, matches_within, matches_between):
    """
    For all pairs of datasets (including a dataset paired with itself), randomly
    select pairs of rows from each dataset and set the name, dob, and ssn of the
    row from the first dataset equal to those values in the second dataset.

    For example, if we are making bookings-0, hmis-0, and bookings-1 datasets,
    we want to create matches for the following pairs:
        - bookings-0 with bookings-0 (creating matching rows within the dataset)
        - bookings-0 with hmis-0 (creating matches between different datasets)
        - bookings-0 with bookings-1
        - hmis-0 with hmis-0
        - hmis-0 with bookings-1
        - bookings-1 with bookings-1
    """
    # iterate through all pairs of datasets
    for dataset1, dataset2 in itertools.product(fake_datasets, repeat=2):
        
        type1 = dataset1['type']
        type2 = dataset2['type']

        # the number of matches to apply depends on whether the rows are being
        # matched within the same dataset or between datasets
        if dataset1 == dataset2:
            num_matches = matches_within
        else:
            num_matches = matches_between

        for _ in range(0, num_matches):
            # select a row from each dataset to match
            row1 = dataset1['data'][random.randint(0, (len(dataset1['data']) - 1))]
            row2 = dataset2['data'][random.randint(0, (len(dataset2['data']) - 1))]

            # use the lookup dictionaries to match the name, dob, and ssn
            for match_field in MATCH_FIELD_INDICES:
                first_index = match_field[type1]
                second_index = match_field[type2]
                row1[first_index] = row2[second_index]

            # set the end date for the earlier row to be before the start date of the second row
            # THIS IS HIDEOUS
            if row1[DATE_FIELD_INDICES[type1]['start_date']] < row2[DATE_FIELD_INDICES[type2]['start_date']]:
                row1[DATE_FIELD_INDICES[type1]['end_date']] = fake.date_time_between(start_date=row1[DATE_FIELD_INDICES[type1]['start_date']], end_date=row2[DATE_FIELD_INDICES[type2]['start_date']])
            elif row2[DATE_FIELD_INDICES[type2]['start_date']] < row1[DATE_FIELD_INDICES[type1]['start_date']]:
                row2[DATE_FIELD_INDICES[type2]['end_date']] = fake.date_time_between(start_date=row2[DATE_FIELD_INDICES[type2]['start_date']], end_date=row1[DATE_FIELD_INDICES[type1]['start_date']])

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
    apply_matches(fake_datasets, matches_within, matches_between)
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
