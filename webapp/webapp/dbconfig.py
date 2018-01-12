import logging
import os
from sqlalchemy.engine.url import URL

if os.environ:
    dbconfig = {
        'host': os.environ.get('PGHOST'),
        'username': os.environ.get('PGUSER'),
        'database': os.environ.get('PGDATABASE'),
        'password': os.environ.get('PGPASSWORD'),
        'port': os.environ.get('PGPORT'),
    }
    dburl = URL('postgres', **dbconfig)
else:
    logging.warning('No config file found, using empty config')
    config = {}
    dburl = ''
