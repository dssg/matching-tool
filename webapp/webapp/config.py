"""Load configuration from a env variable"""
import os
import warnings

config = {
	'base_data_path': os.environ.get('BASE_DATA_PATH', '').replace('\{', '{').replace('\}', '}'),
	'merged_uploads_path': os.environ.get('MERGED_UPLOADS_PATH', '').replace('\{', '{').replace('\}', '}'),
	'base_path': os.environ.get('BASE_PATH', '').replace('\{', '{').replace('\}', '}'),
	'match_cache_path': os.environ.get('MATCH_CACHE_PATH', '').replace('\{', '{').replace('\}', '}'),
 	'raw_uploads_path': os.environ.get('RAW_UPLOADS_PATH', '').replace('\{', '{').replace('\}', '}'),
    'matcher_location': os.environ.get('MATCHER_LOCATION', 'localhost'),
    'matcher_port': os.environ.get('MATCHER_PORT', 5000),
 }

# do some validation of the s3 upload path
for expected_key in ['jurisdiction', 'event_type', 'date', 'upload_id']:
    if '{' + expected_key + '}' not in config['raw_uploads_path']:
        warnings.warn(
            'Environment variable raw_uploads_path {} needs key {} for interpolation'
            .format(config['raw_uploads_path'], expected_key)
        )
