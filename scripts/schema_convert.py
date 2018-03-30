import csv
import re
import json

INPUT_FNAME = "../webapp/schemas/uploader/v5 CSH Project - Data Specifications - Case Charge Data.tsv"
OUTPUT_FNAME = '../webapp/schemas/uploader/case-charge.json'
PKEY_REGEX = '\* Row identifier is a combination of (.*) and should be unique to each row'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

def type_convert(raw_type):
    if raw_type in ['text', 'varchar', 'text-uppercase'] or 'char(' in raw_type:
        return 'string'
    elif raw_type == 'timestamp with timezone':
        return 'string'
    else:
        return raw_type

def constraints(column_name, raw_type, desc, nullable):
    constraints = {}
    if raw_type == 'timestamp with timezone':
        constraints['datetime_with_timezone_hour_only'] = True
    if nullable == 'NO':
        constraints['required'] = True
    enum = enum_from_desc(desc)
    if enum:
        constraints['enum'] = enum

    return constraints


def enum_from_desc(desc):
    match = re.search('\((.*, .*)\)$', desc)
    if match:
        raw_list = match.groups(1)[0].split(', ')
        cleaned_list = [
            row.split(' = ')[0]
            for row in raw_list
        ]
        return cleaned_list
    else:
        return None


if __name__ == '__main__':
    schema = {'fields': []}
    with open(INPUT_FNAME) as f:
        found_fields = False
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if not found_fields and row[0] != 'Data Field Short Description':
                if row[0].startswith('* Row identifier'):
                    match = re.search(PKEY_REGEX, row[0])
                    if match:
                        pkey_string = match.groups(1)[0]
                        schema['primaryKey'] = pkey_string.split(' + ')
                continue
            elif not found_fields:
                found_fields = True
            else:
                schema_type = type_convert(row[2])
                field_constraints = constraints(row[1], row[2], row[3], row[7])
                field = {
                    'name': row[1],
                    'type': schema_type,
                }
                if field_constraints:
                    field['constraints'] = field_constraints
                if schema_type == 'date':
                    field['format'] = DEFAULT_DATE_FORMAT
                schema['fields'].append(field)
    with open(OUTPUT_FNAME, 'w') as f:
        json.dump(schema, f, indent=4)
    print(schema)
