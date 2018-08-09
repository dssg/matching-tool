# Creating or Modifying a Schema

The matching tool can be extended to work with schemas not defined in the initial release. This document defines how this can be done and what limitations are involved.

## Modifying an Existing Schema

To modify the columns or checks in an existing schema:

1. Find the schema in [webapp/schemas/uploader/](https://github.com/dssg/matching-tool/tree/master/webapp/schemas/uploader).

2. Modify the name, datatype, or constraints for an individual field, or the 'primaryKey' that should uniquely define each row. If it is not clear how to modify an individual schema to, for instance, express a constraint in a given way, refer to either the [goodtables-py docs](https://github.com/frictionlessdata/goodtables-py) (the general library used by the matching tool) or the [webapp.validations](https://github.com/dssg/matching-tool/blob/master/webapp/webapp/validations/__init__.py) module (the file where custom checks for the matching tool are defined).

3. If any of the column names, data types, or primary key have changed, you will have to delete the installation's master table as this information is encoded in the master table's schema. Refer your administrator to [Clearing a Master Table for a Schema](../admin/updating.md#clearing-a-master-table-for-a-schema).


## Creating a new Schema

To create a new schema:

1. Create a JSON file containing the schema in [webapp/schemas/uploader/](https://github.com/dssg/matching-tool/tree/master/webapp/schemas/uploader), obeying the same name scheme (`lowercase-separated-by-dashes.json`). Copying an example from one of the existing schemas is recommended. The important parts of the schema:
    - The top-level `name` field simply contains a human-readable name for the schema. This is used in the web UI.
    - The `fields` field contains a list of column names, their datatypes, and any necessary constraints on them. If you have questions about standard constraints that are not clear from the existing .json files, refer to the [goodtables-py docs](https://github.com/frictionlessdata/goodtables-py) (the general library used by the matching tool). If a field is intended to be matched with a field from existing schemas, *use the same field names, types, and constraints* for that field from the existing schemas. The matcher will assume that these are formatted similarly, and you can get poor results if this isn't true.
    - The `primaryKey` field contains a list of column names that uniquely identify a row in the schema. This is important to get right, as this primary key is enforced in the database. If a new row is uploaded that matches the primary key of an existing row, *that row will be updated with the information from the new row*. So ensure that you include enough fields from the schema to uniquely identify events of the event type you are concerned with. For instance, the [jail_bookings](https://github.com/dssg/matching-tool/blob/master/webapp/schemas/uploader/jail-bookings.json) schema can include different rows for different location changes within the jail. Therefore, it has `location_start_date` as part of its primaryKey.
2. (recommended) Update the [schema test file](https://github.com/dssg/matching-tool/blob/master/webapp/webapp/tests/test_schemas.py) with the name of this new schema, and run this test to ensure that your schema doesn't have any structural errors. This helps to do up front as otherwise the error will show up as an internal server error when attempting to upload a file.  To test it:
    - Install [pip](https://pip.pypa.io/en/stable/installing/).
    - `pip install virtualenv`
    - `cd webapp`
    - `virtualenv venv`
    - `source venv/bin/activate`
    - `pip install -r requirements.txt -r requirements_dev.txt`
    - `PYTHONPATH='.' py.test webapp/tests/test_schemas.py`
3. Open the [webapp.validations](https://github.com/dssg/matching-tool/blob/master/webapp/webapp/validations/__init__.py) module.
    - The `CHECKS_BY_SCHEMA` dictionary is where you should add this schema, and a list of the checks that should be activated.  Simply making it `STANDARD_CHECKS` is a good start for schemas that are designed to be similar to the shipped schemas. In the basic case, this is all you should have to do in this file.
    - If you want to add any checks that contain custom logic, you can define them in this file. We will not include a custom check tutorial here, but the examples in that file (any function with the '@check' decorator) and the [goodtables-py docs](https://github.com/frictionlessdata/goodtables-py) will be helpful.
4. Open the [matcher config](https://github.com/dssg/matching-tool/blob/master/matcher/matcher_config.yaml) and make any changes needed. Refer to the [guide on changing the matching config](matching.md) for details, but of note if there are columns in your new schema that you wish to use for matching that aren't present in existing schemas you will have to add them here and configure how they will be used for matching.
5. Have your administrator [install the new code](../admin/updating.md#updating-code) (new schema+validation file updates), and [add your user to the new event type](../admin/updating.md#-user-and-role-management): the event type will be the name of the .json file, dashes replaced with underscores. Alternately, if you have a local installation you can do those steps yourself.
6. At this point, you should be able to upload new files for this schema type, the matcher should be able to produce results, and you can download these results with the original source data with match ids in the results dashboard ('Download Source Events', bottom of the left control panel).

## Limitations when creating a new Schema

Creating a new schema *does not make its events show up on the results dashboard*. The logic for populating the Venn diagrams and results table are highly customized for HMIS Service Stays and Jail Bookings. Adding a third event type to this dashboard raises many interface design questions that are not easy to answer. If you wish to customize this interface, you can refer to [Modifying the Webapp](webapp.md) but know that at this point your version of the code will be highly customized and it will be tough to receive code updates. It is recommended that you import these source events with match ids into your spreadsheet/reporting tool of choice for visualization.
