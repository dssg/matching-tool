"""Load configuration from a env variable"""
import os

config = {
	'merged_uploads_path': os.environ['MERGED_UPLOADS_PATH'],
 	'raw_uploads_path': os.environ['RAW_UPLOADS_PATH']
 }

# do some validation of the s3 upload path
for expected_key in ['jurisdiction', 'event_type', 'date', 'upload_id']:
    if '{' + expected_key + '}' not in config['raw_uploads_path']:
        raise ValueError(
            'Config File raw_uploads_path needs key {} for interpolation'
            .format(expected_key)
        )
