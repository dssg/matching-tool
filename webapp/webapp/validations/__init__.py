from copy import copy
import json
import re
from datetime import datetime
from goodtables import validate, check

from webapp.utils import schema_filename

CHECKS_BY_SCHEMA = {
    'jail_bookings': [
        'composite-primary-key',
        'ssn-or-hashed',
        'inmate-num-or-person-id',
        'partial-dob',
        'genders-list',
        'race-list',
        'ethnicity-list',
        'hair-color-list',
        'eye-color-list',
        'datetime-with-tz',
        'homeless-flag',
        'mental-health-flag',
        'veteran-flag',
        'special-initiative-flag',
        'type-or-format-error',
        'maximum-length-constraint',
    ],
    'hmis_service_stays': [
        'composite-primary-key',
        'ssn-or-hashed',
        'partial-dob',
        'name-data-quality',
        'dob-type',
        'enumerable-constraint',
        'veteran-status',
        'disabling-condition',
        'type-or-format-error',
        'maximum-length-constraint',
        'move-in-date'
    ],
}


@check('inmate-num-or-person-id', type='custom', context='body')
def inmate_num_or_person_id(errors, cells, row_number):
    safe_cells = copy(cells)
    required_cells = [
        cell for cell in safe_cells
        if cell['field'].descriptor.get('name') in ['inmate_number', 'internal_person_id']
    ]
    valid = any(cell['value'] is not None and cell['value'].strip() for cell in required_cells)

    if valid:
        return

    # Add error
    message = 'Row number {}: One of columns {} is needed'.format(
        row_number,
        ', '.join([cell['field'].descriptor.get('name') for cell in required_cells])
    )
    errors.append({
        'code': 'inmate-num-or-person-id-constraint',
        'message': message,
        'row-number': row_number,
        'column-number': required_cells[0]['number'],
    })

def is_good_dob(string):
    regex = '[0-9X]{4}-[0-9X]{2}-[0-9X]{2}'
    match = re.match(regex, string)
    if match:
        return True
    else:
        return False

def is_good_ssn(string):
    if not string:
        return True
    regex = '[0-9X]{9}'
    match = re.match(regex, string)
    if match:
        return True
    else:
        return False

def is_good_hash(string):
    if not string:
        return True
    regex = '[0-9a-f]{40}$'
    match = re.match(regex, string)
    if match:
        return True
    else:
        return False

def is_good_bigrams(string):
    if not string:
        return True
    bigrams = string.split(',')
    if len(bigrams) != 10:
        return False
    return all(is_good_hash(bigram) for bigram in bigrams)


GENDERS = set(['F', 'M', 'MT', 'FT', 'O', 'D', 'R', 'N'])
COMBINED_RACE_ETHNICITIES = set(['W', 'B', 'A', 'I', 'P', 'H', 'O', 'D', 'R', 'N'])
ETHNICITIES = set(['HISPANIC', 'NOT HISPANIC', "INMATE DOESN'T KNOW", "INMATE REFUSED", "DATA NOT COLLECTED"])
HAIR_COLORS = set(['BLD', 'BLK', 'BLN', 'BLU', 'BRO', 'GRY', 'GRN', 'ONG', 'PNK', 'PLE', 'RED', 'SDY', 'WHI', 'XXX'])
EYE_COLORS = set(['BLK', 'BRO', 'GRN', 'MAR', 'PNK', 'BLU', 'GRY', 'HAZ', 'MUL', 'XXX'])
NAME_DATA_QUALITIES = set(['FULL NAME REPORTED', 'PARTIAL, STREET NAME, OR CODE NAME REPORTED', "CLIENT DOESN'T KNOW", 'CLIENT REFUSED'])
DOB_TYPES = set(['FULL DOB REPORTED', 'APPROXIMATE OR PARTIAL DOB REPORTED', "CLIENT DOESN'T KNOW", 'CLIENT REFUSED'])
ADDRESS_DATA_QUALITIES = set(['FULL ADDRESS REPORTED', 'INCOMPLETE OR ESTIMATED ADDRESS REPORTED', "CLIENT DOESN'T KNOW", 'CLIENT REFUSED', 'DATA NOT COLLECTED'])
VETERAN_STATUSES = set(['NO', 'YES', "CLIENT DOESN'T KNOW", 'CLIENT REFUSED', 'DATA NOT COLLECTED'])
DISABLING_CONDITIONS = set(['NO', 'YES', "CLIENT DOESN'T KNOW", 'CLIENT REFUSED', 'DATA NOT COLLECTED'])


def list_membership(errors, cells, row_number, field, valid_list):
    safe_cells = copy(cells)

    cell = [
        cell for cell in safe_cells
        if cell['field'].descriptor.get('name') == field
    ][0]
        
    value = cell.get('value', '')
    if not value:
        value = ''
    else:
        value = value.strip()
    valid = (value == '') or (value in valid_list)

    if valid:
        return

    # Add error
    message = 'Row number {}: {} is {} but should be in list {}'.format(row_number, field, value, valid_list)
    errors.append({
        'code': '{}-list'.format(field.lower().replace('_', '-')),
        'message': message,
        'row-number': row_number,
        'column-number': cell['number'],
    })

@check('genders-list', type='custom', context='body')
def genders_list(errors, cells, row_number):
    return list_membership(errors, cells, row_number, 'sex', GENDERS)

@check('race-list', type='custom', context='body')
def race_list(errors, cells, row_number):
    return list_membership(errors, cells, row_number, 'race', COMBINED_RACE_ETHNICITIES)

@check('secondary-race-list', type='custom', context='body')
def race_list(errors, cells, row_number):
    return list_membership(errors, cells, row_number, 'secondary_race', COMBINED_RACE_ETHNICITIES)

@check('ethnicity-list', type='custom', context='body')
def ethnicity_list(errors, cells, row_number):
    return list_membership(errors, cells, row_number, 'ethnicity', ETHNICITIES)

@check('hair-color-list', type='custom', context='body')
def hair_color_list(errors, cells, row_number):
    return list_membership(errors, cells, row_number, 'hair_color', HAIR_COLORS)

@check('eye-color-list', type='custom', context='body')
def eye_color_list(errors, cells, row_number):
    return list_membership(errors, cells, row_number, 'eye_color', EYE_COLORS)

@check('name-data-quality', type='custom', context='body')
def name_data_quality_list(errors, cells, row_number):
    return list_membership(errors, cells, row_number, 'name_data_quality', NAME_DATA_QUALITIES)

@check('dob-type', type='custom', context='body')
def dob_type_list(errors, cells, row_number):
    return list_membership(errors, cells, row_number, 'dob_type', DOB_TYPES)

@check('address-data-quality', type='custom', context='body')
def address_data_quality_list(errors, cells, row_number):
    return list_membership(errors, cells, row_number, 'address_data_quality', ADDRESS_DATA_QUALITIES)

@check('veteran-status', type='custom', context='body')
def veteran_status_list(errors, cells, row_number):
    return list_membership(errors, cells, row_number, 'veteran_status', VETERAN_STATUSES)

@check('disabling-condition', type='custom', context='body')
def disabling_condition_list(errors, cells, row_number):
    return list_membership(errors, cells, row_number, 'disabling_condition', DISABLING_CONDITIONS)


@check('ssn-or-hashed', type='custom', context='body')
def ssn_or_hashed(errors, cells, row_number):
    safe_cells = copy(cells)
    field_checkers = {
        'ssn': is_good_ssn,
        'ssn_hash': is_good_hash,
        'ssn_bigrams': is_good_bigrams,
    }
    required_cells = [
        cell for cell in safe_cells
        if cell['field'].descriptor.get('name') in field_checkers
    ]
        
    valid = any(
        field_checkers[cell['field'].descriptor.get('name')](cell['value'])
        for cell in required_cells
    )

    if valid:
        return

    # Add error
    message = 'Row number {}: One of columns {} is needed'.format(row_number, list(field_checkers.keys()))
    errors.append({
        'code': 'ssn-or-hashed',
        'message': message,
        'row-number': row_number,
        'column-number': required_cells[0]['number'],
    })

@check('partial-dob', type='custom', context='body')
def partial_dob(errors, cells, row_number):
    safe_cells = copy(cells)

    dob_cell = [
        cell for cell in safe_cells
        if cell['field'].descriptor.get('name') == 'dob'
    ][0]
        
    value = dob_cell.get('value', '')
    if not value:
        value = ''
    else:
        value = value.strip()
    valid = is_good_dob(value)

    if valid:
        return

    # Add error
    message = 'Row number {}: dob should be in format 1982-01-01 (fill in any missing digits with Xs)'.format(row_number)
    errors.append({
        'code': 'partial-dob',
        'message': message,
        'row-number': row_number,
        'column-number': dob_cell['number'],
    })


DATE_FORMAT = '%Y-%m-%d'
def is_good_date(string):
    try:
        datetime.strptime(string, DATE_FORMAT)
        return True
    except ValueError:
        return False

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
def is_good_datetime_with_timezone(string):
    try:
        # our format is non-conformant, we expect only hour but
        # python expects the minutes too, so add the minutes
        datetime.strptime(string + '00', DATETIME_FORMAT)
        return True
    except ValueError:
        return False


def is_good_datetime_with_tzname(string):
    # this is very tough to check for, as the time zone abbreviations
    # aren't easily available. just check the first part
    try: 
        datetime.strptime(string[0:19], '%Y-%m-%dT%H:%M:%S')
        return True
    except ValueError:
        return False


@check('move-in-date', type='custom', context='body')
def move_in_date(errors, cells, row_number):
    safe_cells = copy(cells)
    cell = [
        cell for cell in safe_cells
        if cell['field'].descriptor.get('name') == 'move_in_date'
    ][0]
        
    value = cell.get('value', '')
    if not value:
        value = ''
    else:
        value = value.strip()
    valid = is_good_datetime_with_tzname(value)

    if valid:
        return

    # Add error
    message = 'Row number {}: move_in_date should be in format 1982-01-01T10:00:00 CST'.format(row_number)
    errors.append({
        'code': 'move-in-date',
        'message': message,
        'row-number': row_number,
        'column-number': cell['number'],
    })


@check('datetime-with-tz', type='custom', context='body')
def datetime_with_tz(errors, cells, row_number):
    safe_cells = copy(cells)

    field_names = ['jail_entry_date', 'jail_exit_date', 'relocation_date', 'date_created', 'date_updated']
    not_nullable_fields = ['jail_entry_date']
    my_cells = [
        cell for cell in safe_cells
        if cell['field'].descriptor.get('name') in field_names 
    ]
        
    for cell in my_cells:
        value = cell.get('value', '')
        if not value:
            val = ''
        else:
            val = value.strip()
        nullable = cell['field'].descriptor.get('name') not in not_nullable_fields
        if nullable and not val:
            return

        if not is_good_datetime_with_timezone(val):
            errors.append({
                'code': 'datetime-with-tz',
                'message': 'Row number {}: col {}: datetime {} not in format {}'.format(row_number, cell['field'].descriptor.get('name'), cell['value'], 'YYYY-MM-DDTHH:MM:SS+TZ'),
                'row-number': row_number,
                'column-number': cell['number'],
            })

@check('project-dates', type='custom', context='body')
def project_dates(errors, cells, row_number):
    safe_cells = copy(cells)

    field_names = ['project_start_date', 'project_exit_date']
    not_nullable_fields = []
    my_cells = [
        cell for cell in safe_cells
        if cell['field'].descriptor.get('name') in field_names 
    ]
        
    for cell in my_cells:
        val = cell['value'].strip()
        nullable = cell['field'].descriptor.get('name') not in not_nullable_fields
        if nullable and not val:
            return

        if not is_good_datetime_with_timezone(val):
            errors.append({
                'code': 'date',
                'message': 'Row number {}: col {}: date {} not in format {}'.format(row_number, cell['field'].descriptor.get('name'), cell['value'], 'YYYY-MM-DD'),
                'row-number': row_number,
                'column-number': cell['number'],
            })

BOOLS = ['Y', 'N', '']
@check('homeless-flag', type='custom', context='body')
def homeless(errors, cells, row_number):
    return list_membership(errors, cells, row_number, 'homeless', BOOLS)

@check('mental-health-flag', type='custom', context='body')
def mental_health(errors, cells, row_number):
    return list_membership(errors, cells, row_number, 'mental_health', BOOLS)

@check('veteran-flag', type='custom', context='body')
def veteran(errors, cells, row_number):
    return list_membership(errors, cells, row_number, 'veteran', BOOLS)

@check('special-initiative-flag', type='custom', context='body')
def special_initiative(errors, cells, row_number):
    return list_membership(errors, cells, row_number, 'special_initiative', BOOLS)


@check('composite-primary-key', type='custom', context='body')
class DuplicatePrimaryKey(object):

    # Public

    def __init__(self, **options):
        self.__row_index = {}

    def check_row(self, errors, cells, row_number):

        # Get pointer
        pk_cells = [cell for cell in cells if cell['field'].descriptor.get('primaryKey')]
        all_present = any(cell['value'] is not None and cell['value'].strip() for cell in pk_cells)
        if not all_present:
            # Add error
            message = 'Row number {}: One of columns {} is needed for primary key'.format(row_number, pk_cells)
            errors.append({
                'code': 'composite-primary-key-constraint',
                'message': message,
                'row-number': row_number,
                'column-number': None,
            })
            return
        try:
            pointer = hash(json.dumps([cell['value'] for cell in pk_cells]))
            references = self.__row_index.setdefault(pointer, [])
        except TypeError:
            pointer = None

        # Found pointer
        if pointer:

            # Add error
            if references:
                message = "Row {row_number} has duplicate primary key to row(s) {row_numbers}"
                message = message.format(
                    row_number=row_number,
                    row_numbers=', '.join(map(str, references)))
                errors.append({
                    'code': 'composite-primary-key-constraint',
                    'message': message,
                    'row-number': row_number,
                    'column-number': None,
                })

            # Clear cells
            if references:
                del cells[:]

            # Update references
            references.append(row_number)
