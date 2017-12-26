import unittest
from unittest.mock import patch
import json
from moto import mock_s3_deprecated
import boto
from webapp.tests.utils import rig_test_client,\
    authenticate,\
    create_and_populate_raw_table
from datetime import date
from smart_open import smart_open
from webapp.database import db_session
from webapp.models import Upload, MergeLog
import unicodecsv as csv


GOOD_HMIS_FILE = 'sample_data/uploader_input/hmis-fake-0.csv'

class UploadFileTestCase(unittest.TestCase):
    def test_good_file(self):
        sample_config = {
            'raw_uploads_path': 's3://test-bucket/{jurisdiction}/{event_type}/uploaded/{date}/{upload_id}'
        }
        with patch.dict('webapp.utils.path_config', sample_config):
            with rig_test_client() as app:
                authenticate(app)
                with mock_s3_deprecated():
                    s3_conn = boto.connect_s3()
                    s3_conn.create_bucket('test-bucket')
                    response = app.post(
                        '/api/upload/upload_file?jurisdiction=boone&eventType=hmis_service_stays',
                        content_type='multipart/form-data',
                        data={'file_field': (open(GOOD_HMIS_FILE, 'rb'), 'myfile.csv')}
                    )
                    response_data = json.loads(response.get_data().decode('utf-8'))
                    assert response_data['status'] == 'valid'
                    assert 'exampleRows' in response_data
                    assert 'uploadId' in response_data
                    current_date = date.today().isoformat()
                    expected_s3_path = 's3://test-bucket/boone/hmis_service_stays/uploaded/{}/{}'.format(current_date, response_data['uploadId'])
                    with smart_open(expected_s3_path) as expected_s3_file:
                        with smart_open(GOOD_HMIS_FILE) as source_file:
                            assert expected_s3_file.read() == source_file.read()

                    assert db_session.query(Upload).filter(Upload.id == response_data['uploadId']).one


class MergeFileTestCase(unittest.TestCase):
    def test_good_file(self):
        sample_config = {
            'raw_uploads_path': 's3://test-bucket/{jurisdiction}/{event_type}/uploaded/{date}/{upload_id}',
            'merged_uploads_path': 's3://test-bucket/{jurisdiction}/{event_type}/merged'
        }
        with patch.dict('webapp.utils.path_config', sample_config):
            with rig_test_client() as app:
                authenticate(app)
                with mock_s3_deprecated():
                    s3_conn = boto.connect_s3()
                    s3_conn.create_bucket('test-bucket')
                    # to set up, we want a raw file to have been uploaded
                    # present in s3 and metadata in the database
                    # use the upload file endpoint as a shortcut for setting
                    # this environment up quickly, though this is not ideal
                    response = app.post(
                        '/api/upload/upload_file?jurisdiction=boone&eventType=hmis_service_stays',
                        content_type='multipart/form-data',
                        data={'file_field': (open(GOOD_HMIS_FILE, 'rb'), 'myfile.csv')}
                    )
                    # parse and assert the response just in case something
                    # breaks before the merge stage it will show itself here
                    # and not make us think the merge is broken
                    response_data = json.loads(response.get_data().decode('utf-8'))
                    assert response_data['status'] == 'valid'
                    upload_id = json.loads(response.get_data().decode('utf-8'))['uploadId']

                    # okay, here's what we really want to test.
                    # call the merge endpoint
                    response = app.post('/api/upload/merge_file?uploadId={}'.format(upload_id))
                    response_data = json.loads(response.get_data().decode('utf-8'))
                    assert response_data['status'] == 'valid'
                    # make sure that there is a new merged file on s3
                    expected_s3_path = 's3://test-bucket/boone/hmis_service_stays/merged'
                    with smart_open(expected_s3_path, 'rb') as expected_s3_file:
                        reader = csv.reader(expected_s3_file)
                        assert len([row for row in reader]) == 11

                    # and make sure that the merge log has a record of this
                    assert db_session.query(MergeLog).filter(MergeLog.upload_id == '123-456').one
