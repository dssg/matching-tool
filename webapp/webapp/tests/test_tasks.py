import moto
import boto
from webapp.database import Base
from webapp.tasks import upload_to_s3, copy_raw_table_to_db, upsert_raw_table_to_master
from webapp.utils import makeNamedTemporaryCSV, s3_upload_path, generate_master_table_name
from webapp.models import MergeLog
from unittest.mock import patch
from unittest import TestCase
import testing.postgresql
from webapp.tests.utils import create_and_populate_raw_table
from smart_open import smart_open
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv


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
            sample_config = {
                'raw_uploads_path': 's3://test-bucket/{jurisdiction}/{event_type}/uploaded/{date}/{upload_id}'
            }
            with patch.dict('webapp.utils.app_config', sample_config):
                upload_path = s3_upload_path('boone', 'hmis', '123-567-abc')
                upload_to_s3(upload_path, filename)

        current_date = date.today().isoformat()
        expected_s3_path = 's3://test-bucket/boone/hmis/uploaded/{}/123-567-abc'.format(current_date)
        with smart_open(expected_s3_path) as expected_s3_file:
            content = expected_s3_file.read()
            assert 'val1_1' in content.decode('utf-8')


def test_copy_raw_table_to_db():
    # start with an s3 upload path that we assume to exist
    # and given the event type and jurisdiction
    # we expect the raw table to be copied into a new table with proper schema and return the table name
    with testing.postgresql.Postgresql() as postgresql:
        engine = create_engine(postgresql.url())
        with moto.mock_s3_deprecated():
            s3_conn = boto.connect_s3()
            s3_conn.create_bucket('test-bucket')
            full_s3_path = 's3://test-bucket/123-456'
            with smart_open(full_s3_path, 'w') as writefile:
                writer = csv.writer(writefile)
                for row in [
                    [u'Internal Person ID', u'Internal Event ID', 'Full Name', 'Birthdate', 'SSN'],
                    [u'123456', u'456789', 'Jack T. Ripper', '1896-04-10', '345-45-6789'],
                    [u'123457', u'456780', 'Jack L. Ripper', '1896-04-10', '345-45-6780'],
                ]:
                    writer.writerow(row)
            jurisdiction = 'test'
            event_type = 'test'
            written_raw_table = copy_raw_table_to_db(full_s3_path, event_type, '123-456', engine)
            assert sum(1 for _ in engine.execute('select * from "{}"'.format(written_raw_table))) == 2


MASTER_TABLE_SEED_DATA = [
    [u'123456', u'456789', 'Jack T. Ripper', '1896-04-10', '345-45-6789'],
    [u'123457', u'456780', 'Jack L. Ripper', '1896-04-10', '345-45-6780'],
]

class TestUpsertRawTableToMaster(TestCase):
    jurisdiction = 'test'
    event_type = 'test'

    def get_event_ids_and_names(self, master_table_name, db_engine):
        return [
            row
            for row in db_engine.execute(
                '''select "Internal Event ID", "Full Name" from "{}" order by 1'''.format(master_table_name)
            )
        ]

    def populate_seed_data(self, db_session):
        raw_table_name = '123-456'
        create_and_populate_raw_table('123-456', MASTER_TABLE_SEED_DATA, db_session.bind)
        upsert_raw_table_to_master(raw_table_name, self.jurisdiction, self.event_type, raw_table_name, db_session)

    def test_new_table(self):
        with testing.postgresql.Postgresql() as postgresql:
            engine = create_engine(postgresql.url())
            Base.metadata.create_all(engine)
            db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
            # do initial insert, representing the first time data is uploaded
            self.populate_seed_data(db_session)
            master_table_name = generate_master_table_name(self.jurisdiction, self.event_type)
            result = self.get_event_ids_and_names(master_table_name, db_session)
            assert len(result) == 2
            assert result == [
                ('456780', 'Jack L. Ripper'),
                ('456789', 'Jack T. Ripper'),
            ]
            merge_logs = db_session.query(MergeLog).all()
            assert len(merge_logs) == 1
            assert merge_logs[0].upload_id == '123-456'
            assert merge_logs[0].total_unique_rows == 2
            assert merge_logs[0].new_unique_rows == 2

    def test_update_nonoverlapping(self):
        with testing.postgresql.Postgresql() as postgresql:
            engine = create_engine(postgresql.url())
            Base.metadata.create_all(engine)
            db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
            # do initial insert, representing the first time data is uploaded
            self.populate_seed_data(db_session)
            raw_table_name = '234-567'
            new_data = [
                [u'123458', u'456790', 'Jack F. Ripper', '1896-04-10', '345-45-6789'],
                [u'123459', u'456791', 'Jack R. Ripper', '1896-04-10', '345-45-6780'],
            ]
            create_and_populate_raw_table('234-567', new_data, db_session.bind)
            upsert_raw_table_to_master(raw_table_name, self.jurisdiction, self.event_type, '234-567', db_session)
            master_table_name = generate_master_table_name(self.jurisdiction, self.event_type)
            result = self.get_event_ids_and_names(master_table_name, db_session)
            assert len(result) == 4
            assert result == [
                ('456780', 'Jack L. Ripper'),
                ('456789', 'Jack T. Ripper'),
                ('456790', 'Jack F. Ripper'),
                ('456791', 'Jack R. Ripper'),
            ]
            merge_logs = db_session.query(MergeLog).all()
            assert len(merge_logs) == 2
            assert merge_logs[0].upload_id == '123-456'
            assert merge_logs[1].upload_id == '234-567'
            assert merge_logs[0].total_unique_rows == 2
            assert merge_logs[1].total_unique_rows == 2
            assert merge_logs[0].new_unique_rows == 2
            assert merge_logs[1].new_unique_rows == 2

    def test_update_overlapping(self):
        with testing.postgresql.Postgresql() as postgresql:
            engine = create_engine(postgresql.url())
            Base.metadata.create_all(engine)
            db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
            self.populate_seed_data(db_session)
            # merge in a table with one new row and one row that has the same
            # primary key but a new name: hopefully we won't be seeing much like
            # this in production but we do want to be sure that we use the new
            # data in these cases (for instance, data corrections)
            OLD = '456780'
            UPDATED = '456789'
            NEW = '456791'
            raw_table_name = '234-567'
            new_data = [
                [u'123458', UPDATED, 'Jack F. Ripper', '1896-04-10', '345-45-6789'],
                [u'123459', NEW, 'Jack R. Ripper', '1896-04-10', '345-45-6780'],
            ]
            create_and_populate_raw_table('234-567', new_data, db_session.bind)
            upsert_raw_table_to_master(raw_table_name, self.jurisdiction, self.event_type, '234-567', db_session)
            master_table_name = generate_master_table_name(self.jurisdiction, self.event_type)
            result = self.get_event_ids_and_names(master_table_name, db_session)
            assert len(result) == 3
            # the duplicated event id should only be present once
            assert result == [
                ('456780', 'Jack L. Ripper'),
                ('456789', 'Jack F. Ripper'),
                ('456791', 'Jack R. Ripper'),
            ]
            # let's check the timestamps
            timestamp_result = dict((row[0], (row[1], row[2])) for row in db_session.execute('''
                select "Internal Event ID", "inserted_ts", "updated_ts" from {}
                '''.format(master_table_name)
            ))
            # created timestamp of an old row that was not updated should be the same as an old row that was updated
            assert timestamp_result[OLD][0] == timestamp_result[UPDATED][0]
            # updated timestamp of an old row that was not updated should be lower than an old row that was updated
            assert timestamp_result[OLD][1] < timestamp_result[UPDATED][1]
            # created and updated timestamps of totally new rows should be equivalent
            assert timestamp_result[NEW][0] == timestamp_result[NEW][1]

            merge_logs = db_session.query(MergeLog).all()
            assert len(merge_logs) == 2
            assert merge_logs[0].upload_id == '123-456'
            assert merge_logs[1].upload_id == '234-567'
            assert merge_logs[0].total_unique_rows == 2
            assert merge_logs[1].total_unique_rows == 2
            assert merge_logs[0].new_unique_rows == 2
            assert merge_logs[1].new_unique_rows == 1
