import moto
import boto
from webapp.tasks import upload_to_s3
from webapp.utils import makeNamedTemporaryCSV
from smart_open import smart_open
from datetime import date


def test_upload_to_s3():
    # smart_open uses boto2, new moto defaults to boto3
    # so use the _deprecated suffix
    with moto.mock_s3_deprecated():
        s3_conn = boto.connect_s3()
        s3_conn.create_bucket('test-bucket')
        with makeNamedTemporaryCSV([
            [u'col1', u'col2'],
            [u'val1_1', u'val1_2'],
            [u'v\xedl2_1', u'val2_2'],
        ]) as filename:
            upload_to_s3(
                path_template='s3://test-bucket/{jurisdiction}/{service_provider}/uploaded/{date}/{upload_id}',
                upload_id='123-567-abc',
                jurisdiction='boone',
                service_provider='hmis',
                local_filename=filename
            )

        current_date = date.today().isoformat()
        expected_s3_path = 's3://test-bucket/boone/hmis/uploaded/{}/123-567-abc'.format(current_date)
        with smart_open(expected_s3_path) as expected_s3_file:
            content = expected_s3_file.read()
            assert 'val1_1' in content.decode('utf-8')
