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
