# csh
Integrating HMIS and criminal-justice data

## Requirements

Postgres database
Python 3

## Quick Start

1. `pip install -r requirements.txt`
2. `cp example_database.yaml database.yaml` and modify with your database information
3. `cp example_flask_config.yaml flask_config.yaml` and modify to match your tastes (in production, change the SECRET and SECURITY_PASSWORD_SALT!)
4. python webapp/app.py

## Adding Users
The Flask-Security library is utilized, and it comes with CLI scripts for user and role management. Example:

`FLASK_APP=webapp/app.py flask users create email@example.com`

## Adding Roles
The generic Flask-Security command for adding a role looks like this:

`FLASK_APP=webapp/app.py flask roles create <rolename>`

This application, however, has a special format for roles. A role is split into a jurisdiction and a service provider, such as `boone_hmis` or `clark_jail`. Example:

`FLASK_APP=webapp/app.py flask roles create boone_hmis`

will create a role for Boone County's HMIS data.

## Adding Users to Roles

The following will add a the user we created above to the role we created above.

`FLASK_APP=webapp/app.py flask roles add email@example.com boone_hmis`

## Removing Users from Roles

The following will remove the user we created above from the role we created above.

`FLASK_APP=webapp/app.py flask roles remove email@example.com boone_hmis`
