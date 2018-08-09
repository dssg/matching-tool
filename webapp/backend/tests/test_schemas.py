from tableschema import Schema
from backend import SCHEMA_DIRECTORY


def test_all_schemas():
    schema_files = [
        'hmis-service-stays',
        'hmis-aliases',
        'by-name-list',
        'jail-bookings',
        'jail-booking-aliases',
        'jail-booking-charges',
        'case-charges'
    ]
    for schema_file in schema_files:
        schema = Schema(SCHEMA_DIRECTORY + schema_file + '.json')
        assert not schema.errors
