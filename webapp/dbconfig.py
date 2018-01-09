import logging
import os
import yaml
from sqlalchemy.engine.url import URL

profile_file = os.environ.get('PROFILE', 'database.yaml')

if os.path.exists(profile_file):
    with open(profile_file) as f:
        config = yaml.load(f)
        dbconfig = {
            'host': config['PGHOST'],
            'username': config['PGUSER'],
            'database': config['PGDATABASE'],
            'password': config['PGPASSWORD'],
            'port': config['PGPORT'],
        }
        dburl = URL('postgres', **dbconfig)

else:
    logging.warning('No config file found, using empty config')
    config = {}
    dburl = ''
