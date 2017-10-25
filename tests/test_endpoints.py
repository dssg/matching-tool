import unittest
from unittest.mock import patch
import json
from moto import mock_s3_deprecated
import boto
from tests.utils import rig_test_client, authenticate
from datetime import date
from smart_open import smart_open
from webapp.database import db_session
from webapp.models import Upload


class UploadFileTestCase(unittest.TestCase):
    def test_good_file(self):
        sample_config = {
            'raw_uploads_path': 's3://test-bucket/{jurisdiction}/{service_provider}/uploaded/{date}/{upload_id}'
        }
        with patch.dict('webapp.app.path_config', sample_config):
            with rig_test_client() as app:
                authenticate(app)
                with mock_s3_deprecated():
                    s3_conn = boto.connect_s3()
                    s3_conn.create_bucket('test-bucket')
                    response = app.post(
                        '/upload_file?jurisdiction=boone&serviceProvider=hmis',
                        content_type='multipart/form-data',
                        data={'file_field': (open('hmis-good.csv', 'rb'), 'myfile.csv')}
                    )
                    response_data = json.loads(response.get_data().decode('utf-8'))
                    assert response_data['status'] == 'valid'
                    assert 'exampleRows' in response_data
                    assert 'uploadId' in response_data
                    current_date = date.today().isoformat()
                    expected_s3_path = 's3://test-bucket/boone/hmis/uploaded/{}/{}'.format(current_date, response_data['uploadId'])
                    with smart_open(expected_s3_path) as expected_s3_file:
                        with smart_open('hmis-good.csv') as source_file:
                            assert expected_s3_file.read() == source_file.read()

                    assert db_session.query(Upload).filter(Upload.id == response_data['uploadId']).one
