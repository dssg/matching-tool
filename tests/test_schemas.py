from tableschema import Schema

def test_all_schemas():
    schema_files = ['hmis-service-stays-schema.json', 'jail-bookings-schema.json']
    for schema_file in schema_files:
        schema = Schema(schema_file)
        assert not schema.errors
