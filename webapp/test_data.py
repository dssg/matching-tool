from goodtables import validate
from webapp.validations import composite_primary_key
from webapp.utils import load_schema_file
from webapp import tasks
from collections import Counter
import argparse
import os

parser = argparse.ArgumentParser(description='Test a DDJ schema file')
parser.add_argument('--jurisdiction', dest='jurisdiction', type=str)
parser.add_argument('--event-type', dest='event_type', type=str)
parser.add_argument('--row-limit', dest='row_limit', type=int)
parser.add_argument('--print-errors', dest='print_errors_of_type', type=str)

args = parser.parse_args()
path = '{}/{}/{}'.format(
    os.environ['MATCHING_DATA_PATH'],
    args.jurisdiction,
    args.event_type
)
print(args.jurisdiction)
print(args.event_type)
print(args.row_limit)
print(args.print_errors_of_type)
schema = load_schema_file(args.event_type)
colname_lookup = dict(
    (colindex+1, field['name'])
    for colindex, field in enumerate(schema['fields'])
)
print(colname_lookup)
report = tasks.fill_and_validate(args.event_type, path, args.row_limit)
print(report['error-count'])
counter = Counter()
print('\n\n\n\n\n')
print('------------------------------')
print('PRINTING FIRST 10 ERRORS')
print('------------------------------')
print('\n\n\n\n\n')
print(counter)
for error_num in range(0, min(report['error-count'], 10)):
    print(report['tables'][0]['errors'][error_num])
for error in report['tables'][0]['errors']:
    counter[(error['code'], colname_lookup[error['column-number']])] += 1
if(args.print_errors_of_type):
    print('\n\n\n\n\n')
    print('------------------------------')
    print('PRINTING ERRORS OF TYPE')
    print('------------------------------')
    print('\n\n\n\n\n')
    for error in report['tables'][0]['errors']:
        if error['code'] == args.print_errors_of_type:
            print(error)

print('\n\n\n\n\n')
print('------------------------------')
print('PRINTING COUNTER')
print('------------------------------')
print('\n\n\n\n\n')
print(counter)
