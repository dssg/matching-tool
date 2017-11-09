from __future__ import division

import random
import csv
from functools import partial
from faker import Faker

fake = Faker()

fakers = [
    ('Internal Person ID', lambda: str(random.randint(0, 10000000))),
    ('Internal Event ID', lambda: str(random.randint(0, 100000000))),
    ('Inmate Number', lambda: str(random.randint(0, 10000000))),
    ('First Name', fake.first_name),
    ('Last Name', fake.last_name),
    ('Birthdate', partial(fake.date_time_between, start_date='-75y', end_date='-18y')),
    ('SSN', fake.ssn),
    ('Fingerprint ID', lambda: str(random.randint(0, 1000000))),
    ('Race/Ethnicity', lambda: random.choice(['white', 'black', 'amindian', 'asian', 'pacisland', 'other'])),
    ('Ethnicity', lambda: random.choice(['hispanic', 'nonhispanic'])),
    ('Jail Entry Date', partial(fake.date_time_between, start_date='-1y', end_date='-90d')),
    ('Jail Exit Date', partial(fake.date_time_between, start_date='-90d', end_date='-1d')),
]


def fake_person():
    return [fake_func() for _, fake_func in fakers]


def main():
    with open('bookings-fake.csv', 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        headers = [column_name for column_name, _ in fakers]
        writer.writerow(headers)
        for i in range(0, 100):
            writer.writerow(fake_person())

if __name__ == '__main__':
    main()
