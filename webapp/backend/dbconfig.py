import logging
import os
from sqlalchemy.engine.url import URL

if os.environ:
    dbconfig = {
        'host': os.environ.get('POSTGRES_HOST'),
        'username': os.environ.get('POSTGRES_USER'),
        'database': os.environ.get('POSTGRES_DATABASE'),
        'password': os.environ.get('POSTGRES_PASSWORD'),
        'port': os.environ.get('POSTGRES_PORT'),
    }
    dburl = URL('postgres', **dbconfig)
else:
    logging.warning('No config file found, using empty config')
    config = {}
    dburl = ''
