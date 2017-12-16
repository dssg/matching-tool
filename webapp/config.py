"""Load configuration from a yaml file"""
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.load(f)

# do some validation of the s3 upload path
for expected_key in ['jurisdiction', 'service_provider', 'date', 'upload_id']:
    if '{' + expected_key + '}' not in config['raw_uploads_path']:
        raise ValueError(
            'Config File raw_uploads_path needs key {} for interpolation'
            .format(expected_key)
        )
