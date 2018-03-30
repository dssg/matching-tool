# csh
Integrating HMIS and criminal-justice data

## Requirements

- Postgres database
- Python 3

## Setup before running

1. `pip install -r requirements.txt` (and requirements_dev.txt most likely, if you want to develop or run unit tests)
2. `cp example_database.yaml database.yaml` and modify with your database information
3. `cp example_flask_config.yaml flask_config.yaml` and modify to match your tastes (in production, change the SECRET and SECURITY_PASSWORD_SALT!)
4. `cp example_config.yaml config.yaml` and modify to match the resources (for instance, s3 buckets) available to you.
5. `alembic upgrade head` to upgrade the Postgres database
6. Install NodeJS (https://nodejs.org/en/)
7. `cd frontend && npm install` to install dependencies (the initial install will take a few minutes, go have a snack!)

## Run the app
1. `cd frontend && npm run start` to watch JS files and recompile
2. `python webapp/app.py` to run the Flask server

## S3 Credentials
This project utilizes [smart_open](https://github.com/RaRe-Technologies/smart_open) for S3 connectivity, which itself uses [Boto 2](http://boto.cloudhackers.com/en/latest/). Credentials are handled at the Boto level, so you may utilize either environment variables or Boto config files to pass credentials to the application.

See more details at the [Boto Docs](http://boto.cloudhackers.com/en/latest/boto_config_tut.html)

For development, we recommend using moto's [standalone server mode](https://github.com/spulec/moto#stand-alone-server-mode). The server is in requirements_dev already, so here's a quick guide without changing any code:

1. Create a `~/.boto` file with:

```
[Boto]
is_secure = False
https_validate_certificates = False
proxy_port = 3000
proxy = 127.0.0.1

[Credentials]
aws_access_key_id = fake
aws_secret_access_key = fake
```
2. `moto_server s3 -p3000`
3. Create the bucket specified in your config.yaml file. You will have to do this each time you start the fake server. The example has 'your-bucket', so for instance you can run this in a python console:

```
import boto
conn = boto.connect_s3()
conn.create_bucket('your-bucket')
```

## User Management
The Flask-Security library is utilized, and it comes with CLI scripts for user and role management. 

### Adding Users
Adding a user to the database:

`FLASK_APP=webapp/app.py flask users create email@example.com`

### Adding Roles
The generic Flask-Security command for adding a role looks like this:

`FLASK_APP=webapp/app.py flask roles create <rolename>`

This application, however, has a special format for roles. A role is split into a jurisdiction and a event type, such as `boone_hmis` or `clark_jail`. Example:

`FLASK_APP=webapp/app.py flask roles create boone_hmis`

will create a role for Boone County's HMIS data.

### Adding Users to Roles

The following will add a the user we created above to the role we created above.

`FLASK_APP=webapp/app.py flask roles add email@example.com boone_hmis`

### Removing Users from Roles

The following will remove the user we created above from the role we created above.

`FLASK_APP=webapp/app.py flask roles remove email@example.com boone_hmis`


## Adding a Schema

1. Make a schema file (guide to come), put in `webapp/schemas/uploader/` with dashes between words

2. Add to `webapp/webapp/tests/test_schemas.py` and run test to validate schema

3. Add entry to `webapp/webapp/validations/__init__.py`:CHECKS_BY_SCHEMA with desired checks, key being same as filename but with underscores between words

4. Create a role for all jurisdictions that can use this schema, and add any desired users to this role.  For instance, to let testuser@example.com upload files for test county, run this outside of a running container:

`docker exec -it webapp flask roles create test_by_name_list`
`docker exec -it webapp flask roles add testuser@example.com test_by_name_list`

5. Restart the webapp and webapp_worker containers to pick up the changes


## Running All Tests
This project uses [Tox](https://tox.readthedocs.io/en/latest/) to run both the Python and JS test suites. This is recommended before pushing commits. To run all tests,

1. Install tox: `pip install tox`

2. Run tox in the repository root: `tox`

## Dev Front-end Notes

Matching Tool uses NodeJS and Webpack to organize and bundle frontend dependencies.

### Troubleshooting

Sometimes node and npm versions from package managers are ancient and need to be upgraded before installation will work.

To upgrade node to the latest stable version:

1. `sudo npm cache clean -f`

2. `sudo npm install -g n`

3. `sudo n stable`

To upgrade npm:

1. `sudo npm install npm@latest -g`

### During development
`npm run start` will start a webpack '--watch' command that watches your javascript and compiles it to webapp/static/output.js. The initial startup will probably take 10-15 seconds, but every time you save a javascript file the recompilation will be much quicker.

New components can be added in the `frontend/components` directory. There is a directory for each component, because soon (not yet) we will start bundling styles in individual component directories. Other components will be able to import your new component right away, but if you would like the component to made available *globally* (in other words, a Flask template), you will have to add this to `frontend/index.js`

### Running front-end tests
Jest is used for front-end tests. There are two convenience npm commands available for running tests:

- `npm run test` to run the test suite once
- `npm run test:watch` to run jest in watch mode, which will re-run tests upon file save

Tests are located in `frontend/__tests__`. For tests that encompass web service calls, add the mocked output in `endpoint_examples`, and use it similarly to `actions.js#syncRoleAction`, so the JSON interface can remain in sync with the Flask server's expectations.

### Installing new modules
In the `frontend` directory, install the package you want with `npm install --save <pkg-name>`. The --save option will persist this change to package.json.

