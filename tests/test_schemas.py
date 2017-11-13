from tableschema import Schema

def test_all_schemas():
    schema_files = ['hmis-schema.json', 'jail-schema.json']
    for schema_file in schema_files:
        schema = Schema(schema_file)
        assert not schema.errors
