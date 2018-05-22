"""Load configuration from a env variable"""
import os

config = {
	'base_data_path': os.environ['BASE_DATA_PATH'].replace('\{', '{').replace('\}', '}'),
	'merged_uploads_path': os.environ['MERGED_UPLOADS_PATH'].replace('\{', '{').replace('\}', '}'),
 	'raw_uploads_path': os.environ['RAW_UPLOADS_PATH'].replace('\{', '{').replace('\}', '}'),
    'matcher_location': os.environ['MATCHER_LOCATION'],
    'matcher_port': os.environ['MATCHER_PORT']
 }

# do some validation of the s3 upload path
for expected_key in ['jurisdiction', 'event_type', 'date', 'upload_id']:
    if '{' + expected_key + '}' not in config['raw_uploads_path']:
        raise ValueError(
            'Environment variable raw_uploads_path {} needs key {} for interpolation'
            .format(config['raw_uploads_path'], expected_key)
        )
