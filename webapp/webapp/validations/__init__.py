from copy import copy
import json
import re
from datetime import datetime
from goodtables import check

CHECKS_BY_SCHEMA = {
    'jail_bookings': [
        'composite-primary-key',
        'ssn-or-hashed',
        'inmate-num-or-person-id',
        'booking-num-or-event-id',
        'partial-dob',
        'datetime-with-tz',
        'type-or-format-error',
        'enumerable-constraint',
        'enumerable-maybe-list',
        'maximum-length-constraint',
        'required-ignoring-pk'
    ],
    'hmis_service_stays': [
        'composite-primary-key',
        'ssn-or-hashed',
        'partial-dob',
        'enumerable-constraint',
        'enumerable-maybe-list',
        'type-or-format-error',
        'maximum-length-constraint',
        'required-ignoring-pk'
    ],
}


@check('inmate-num-or-person-id', type='custom', context='body')
def inmate_num_or_person_id(errors, cells, row_number):
    """One of the inmate number or internal_person_id columns must be present and with a value"""
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


@check('booking-num-or-event-id', type='custom', context='body')
def booking_num_or_event_id(errors, cells, row_number):
    """One of the booking number or internal_event_id columns must be present and with a value"""
    safe_cells = copy(cells)
    required_cells = [
        cell for cell in safe_cells
        if cell['field'].descriptor.get('name') in ['booking_number', 'internal_event_id']
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
        'code': 'booking-num-or-event-id-constraint',
        'message': message,
        'row-number': row_number,
        'column-number': required_cells[0]['number'],
    })


def is_good_dob(string):
    if not string:
        return True
    regex = '^[0-9X]{4}-[0-9X]{2}-[0-9X]{2}$'
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


@check('ssn-or-hashed', type='custom', context='body')
def ssn_or_hashed(errors, cells, row_number):
    """Check the variety of SSN columns with their appropriate checks"""
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


@check('required-ignoring-pk', type='custom', context='body')
def required_ignoring_pk(errors, cells, row_number):
    """The goodtables required-constraint also includes composite primary key columns, which we don't want. Here we reimplement it, only looking at the columns which are marked 'required' by the schema itself.
    """
    safe_cells = copy(cells)
    required_cells = [
        cell for cell in safe_cells
        if cell['field'].descriptor.get('constraints', {}).get('required', False)
    ]

    for cell in required_cells:
        if not cell['value'] or not cell['value'].strip():
            message = 'Row number {}: column {} is needed'.format(
                row_number,
                cell['field'].descriptor.get('name')
            )
            errors.append({
                'code': 'required-ignoring-pk',
                'message': message,
                'row-number': row_number,
                'column-number': cell['number'],
            })


@check('partial-dob', type='custom', context='body')
def partial_dob(errors, cells, row_number):
    """Check that the DOB is valid (it is nullable, and missing digits can be filled with Xs"""
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


@check('datetime-with-tz', type='custom', context='body')
def datetime_with_tz(errors, cells, row_number):
    """Check a datetime with a timezone offset. We use a slightly different format than is expressible in Python datetime formats, so we can't use the built in datetime format check for this.
    """
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

@check('enumerable-maybe-list', type='custom', context='body')
def enumerable_maybe_list(errors, cells, row_number):
    """Check that each value in a field matches the given enum, or if multiple values are in the cell separated by a comma and space, check each of those values
    """
    safe_cells = copy(cells)

    cells_with_enums = [
        cell
        for cell in safe_cells
        if cell['field'].descriptor.get('constraints', {}).get('enum_maybe_list', None)
    ]
    for cell in cells_with_enums:
        enum = cell['field'].descriptor['constraints']['enum_maybe_list']
        value = cell.get('value', '')
        if not value:
            value = ''
        else:
            value = str(value).strip()

        maybe_list = value.split(',')
        for value in maybe_list:
            valid = (value.strip() == '') or (value.strip() in enum)
            if not valid:
                # Add error
                message = 'Row number {}: {} is {} but should be in list {}'.format(row_number, cell['field'].descriptor.get('name'), value.strip(), enum)
                errors.append({
                    'code': 'enum-maybe-list-constraint',
                    'message': message,
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
