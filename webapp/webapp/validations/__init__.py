from copy import copy
import json
import re
from datetime import datetime
from goodtables import check

STANDARD_CHECKS = [
    'composite-primary-key',
    'partial-dob',
    'type-or-format-error',
    'enumerable-constraint',
    'pattern-constraint',
    'enumerable-maybe-list',
    'maximum-length-constraint',
    'required-ignoring-pk',
    'datetime-maybe-with-tz',
    'lname-or-fullname'
]

CHECKS_BY_SCHEMA = {
    'jail_bookings': STANDARD_CHECKS + [
        'inmate-num-or-person-id',
        'booking-num-or-event-id',
    ],
    'hmis_service_stays': STANDARD_CHECKS,
    'by_name_list': STANDARD_CHECKS,
    'hmis_aliases': STANDARD_CHECKS,
    'jail_booking_aliases': STANDARD_CHECKS,
    'jail_booking_charges': STANDARD_CHECKS + [
        'inmate-num-or-person-id',
        'booking-num-or-event-id',
    ],
    'case_charges': STANDARD_CHECKS,
}


@check('inmate-num-or-person-id', type='custom', context='body')

def inmate_num_or_person_id(*args, **kwargs):
    return one_of_group(['inmate_number', 'internal_person_id'], *args, **kwargs)


@check('booking-num-or-event-id', type='custom', context='body')
def booking_num_or_event_id(*args, **kwargs):
    return one_of_group(['booking_number', 'internal_event_id'], *args, **kwargs)


@check('lname-or-fullname', type='custom', context='body')
def last_name_or_full_name(*args, **kwargs):
    return one_of_group(['last_name', 'full_name'], *args, **kwargs)



def one_of_group(columns_in_group, errors, cells, row_number):
    """One of a list of columns should be present and populated"""
    safe_cells = copy(cells)
    required_cells = [
        cell for cell in safe_cells
        if cell['field'].descriptor.get('name') in columns_in_group
    ]
    valid = any(cell['value'] is not None and cell['value'].strip() for cell in required_cells)

    if valid:
        return

    # Add error
    message = 'Row number {}: One of columns {} is needed to be both present and populated'.format(
        row_number,
        columns_in_group
    )
    errors.append({
        'code': 'one-of-group-constraint',
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

    affected_cells = [
        cell
        for cell in safe_cells
        if cell['field'].descriptor.get('constraints', {}).get('partial_dob', False)
    ]

    for affected_cell in affected_cells:
        value = affected_cell.get('value', '')
        if not value:
            value = ''
        else:
            value = value.strip()
        valid = is_good_dob(value)

        if valid:
            return

        # Add error
        message = 'Row number {}: The value {} in  column {} is not in format YYYY-MM-DD (fill in any missing digits with Xs)'.format(
            row_number,
            value,
            affected_cell['number']
        )
        errors.append({
            'code': 'partial-dob',
            'message': message,
            'row-number': row_number,
            'column-number': affected_cell['number'],
        })


DATE_FORMAT = '%Y-%m-%d'
def is_good_date(string):
    try:
        datetime.strptime(string, DATE_FORMAT)
        return True
    except ValueError:
        return False



SUPPORTED_DATETIME_FORMATS = [
    '%Y-%m-%dT%H:%M:%S',
    '%Y-%m-%d %H:%M:%S',
    DATE_FORMAT,
]
def is_good_datetime_with_timezone(string):
    for dt_format in SUPPORTED_DATETIME_FORMATS:
        try:
            datetime.strptime(string[0:19], dt_format)
            return True
        except ValueError:
            continue
    return False




@check('datetime-maybe-with-tz', type='custom', context='body')
def datetime_maybe_with_tz(errors, cells, row_number):
    """Check a datetime with a timezone offset. We use a slightly different format than is expressible in Python datetime formats, so we can't use the built in datetime format check for this.
    """
    safe_cells = copy(cells)

    affected_cells = [
        cell
        for cell in safe_cells
        if cell['field'].descriptor.get('constraints', {}).get('datetime_with_timezone_hour_only', False)
    ]

    for cell in affected_cells:
        value = cell.get('value', '')
        if not value:
            val = ''
        else:
            val = value.strip()
        # assume fields are nullable. required constraint should be covered by another check
        if not val:
            return

        if not is_good_datetime_with_timezone(val):
            errors.append({
                'code': 'datetime-maybe-with-tz',
                'message': 'Row number {}: The value {} in  column {} should be either formats {} or {}'.format(
                    row_number,
                    cell['value'],
                    cell['number'],
                    'YYYY-MM-DDTHH:MM:SS+TZ',
                    'YYYY-MM-DDTHH:MM:SS'
                ),
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
                message = "Row number {row_number}: The value {value} in  column {pk_name} has duplicate primary key to row(s) {row_numbers}"
                message = message.format(
                    row_number=row_number,
                    value=','.join([cell['value'] for cell in pk_cells]),
                    pk_name=','.join([cell['field'].descriptor.get('name') for cell in pk_cells]),
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
