import moto
import boto
from webapp.database import Base
from webapp.models import MergeLog, MatchLog
import time
from unittest.mock import patch
from unittest import TestCase
import testing.postgresql
from webapp.tasks import \
    upload_to_s3,\
    copy_raw_table_to_db,\
    upsert_raw_table_to_master,\
    validate_header,\
    write_match_log,\
    write_upload_log,\
    write_matches_to_db
from webapp.utils import makeNamedTemporaryCSV, s3_upload_path, generate_master_table_name, generate_matched_table_name
from webapp.tests.utils import create_and_populate_raw_table, rig_test_client, create_and_populate_matched_table
from smart_open import smart_open
from datetime import date, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv
import unicodecsv


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
                    [u'internal_person_id', u'internal_event_id', u'location_id', 'full_name', 'birthdate', 'ssn'],
                    [u'123456', u'456789', u'A345', 'Jack T. Ripper', '1896-04-10', '345-45-6789'],
                    [u'123457', u'456780', u'A345', 'Jack L. Ripper', '1896-04-10', '345-45-6780'],
                    [u'123457', u'456780', u'A346', 'Jack L. Ripper', '1896-04-10', '345-45-6780'],
                ]:
                    writer.writerow(row)
            jurisdiction = 'test'
            event_type = 'test'
            written_raw_table = copy_raw_table_to_db(full_s3_path, event_type, '123-456', engine)
            assert sum(1 for _ in engine.execute('select * from "{}"'.format(written_raw_table))) == 3

class RawTableDuplicateCheck(TestCase):
    def test_copy_raw_table_to_db_duplicate(self):
        # we create a file with duplicates
        # upon copying to raw table, we expect the duplicate error to be tripped
        # and presented in a user-friendly format
        with testing.postgresql.Postgresql() as postgresql:
            engine = create_engine(postgresql.url())
            with moto.mock_s3_deprecated():
                s3_conn = boto.connect_s3()
                s3_conn.create_bucket('test-bucket')
                full_s3_path = 's3://test-bucket/123-456'
                with smart_open(full_s3_path, 'w') as writefile:
                    writer = csv.writer(writefile)
                    for row in [
                    [u'internal_person_id', u'internal_event_id', u'location_id', 'full_name', 'birthdate', 'ssn'],
                        [u'123456', u'456789', u'A345', 'Jack T. Ripper', '1896-04-10', '345-45-6789'],
                        [u'123457', u'456780', u'A345', 'Jack L. Ripper', '1896-04-10', '345-45-6780'],
                        [u'123457', u'456780', u'A345', 'Jack L. Ripper', '1896-04-10', '345-45-6780'],
                        [u'123457', u'456780', u'A346', 'Jack L. Ripper', '1896-04-10', '345-45-6780'],
                    ]:
                        writer.writerow(row)
                jurisdiction = 'test'
                event_type = 'test'
                with self.assertRaisesRegexp(ValueError, expected_regex=r'.*line 4.*internal_event_id, location_id.*456780.*A345.*'):
                    copy_raw_table_to_db(full_s3_path, event_type, '123-456', engine)


MASTER_TABLE_SEED_DATA = [
    [u'123456', u'456789', u'A345', 'Jack T. Ripper', '1896-04-10', '345-45-6789'],
    [u'123457', u'456780', u'A345', 'Jack L. Ripper', '1896-04-10', '345-45-6780'],
    [u'123457', u'456780', u'A346', 'Jack L. Ripper', '1896-04-10', '345-45-6780'],
]

class TestUpsertRawTableToMaster(TestCase):
    jurisdiction = 'test'
    event_type = 'test'

    def get_pks_and_names(self, master_table_name, db_engine):
        return [
            row
            for row in db_engine.execute(
                '''select "internal_event_id", "location_id", "full_name" from "{}" order by 1, 2'''.format(master_table_name)
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
            result = self.get_pks_and_names(master_table_name, db_session)
            assert len(result) == 3
            assert result == [
                ('456780', 'A345', 'Jack L. Ripper'),
                ('456780', 'A346', 'Jack L. Ripper'),
                ('456789', 'A345', 'Jack T. Ripper'),
            ]
            merge_logs = db_session.query(MergeLog).all()
            assert len(merge_logs) == 1
            assert merge_logs[0].upload_id == '123-456'
            assert merge_logs[0].total_unique_rows == 3
            assert merge_logs[0].new_unique_rows == 3

    def test_update_nonoverlapping(self):
        with testing.postgresql.Postgresql() as postgresql:
            engine = create_engine(postgresql.url())
            Base.metadata.create_all(engine)
            db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
            # do initial insert, representing the first time data is uploaded
            self.populate_seed_data(db_session)
            raw_table_name = '234-567'
            new_data = [
                [u'123458', u'456790', 'A345', 'Jack F. Ripper', '1896-04-10', '345-45-6789'],
                [u'123459', u'456791', 'A345', 'Jack R. Ripper', '1896-04-10', '345-45-6780'],
            ]
            create_and_populate_raw_table('234-567', new_data, db_session.bind)
            upsert_raw_table_to_master(raw_table_name, self.jurisdiction, self.event_type, '234-567', db_session)
            master_table_name = generate_master_table_name(self.jurisdiction, self.event_type)
            result = self.get_pks_and_names(master_table_name, db_session)
            assert len(result) == 5
            assert result == [
                ('456780', 'A345', 'Jack L. Ripper'),
                ('456780', 'A346', 'Jack L. Ripper'),
                ('456789', 'A345', 'Jack T. Ripper'),
                ('456790', 'A345', 'Jack F. Ripper'),
                ('456791', 'A345', 'Jack R. Ripper'),
            ]
            merge_logs = db_session.query(MergeLog).all()
            assert len(merge_logs) == 2
            assert merge_logs[0].upload_id == '123-456'
            assert merge_logs[1].upload_id == '234-567'
            assert merge_logs[0].total_unique_rows == 3
            assert merge_logs[1].total_unique_rows == 2
            assert merge_logs[0].new_unique_rows == 3
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
                [u'123458', UPDATED, 'A345', 'Jack F. Ripper', '1896-04-10', '345-45-6789'],
                [u'123459', NEW, 'A345', 'Jack R. Ripper', '1896-04-10', '345-45-6780'],
            ]
            create_and_populate_raw_table('234-567', new_data, db_session.bind)
            upsert_raw_table_to_master(raw_table_name, self.jurisdiction, self.event_type, '234-567', db_session)
            master_table_name = generate_master_table_name(self.jurisdiction, self.event_type)
            result = self.get_pks_and_names(master_table_name, db_session)
            assert len(result) == 4
            # the duplicated event id should only be present once
            assert result == [
                ('456780', 'A345', 'Jack L. Ripper'),
                ('456780', 'A346', 'Jack L. Ripper'),
                ('456789', 'A345', 'Jack F. Ripper'),
                ('456791', 'A345', 'Jack R. Ripper'),
            ]
            # let's check the timestamps
            timestamp_result = dict((row[0], (row[1], row[2])) for row in db_session.execute('''
                select "internal_event_id", "inserted_ts", "updated_ts" from {}
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
            assert merge_logs[0].total_unique_rows == 3
            assert merge_logs[1].total_unique_rows == 2
            assert merge_logs[0].new_unique_rows == 3
            assert merge_logs[1].new_unique_rows == 1

class ValidateHeaderTest(TestCase):
    def test_validate_header_fields_missing(self):
        # the 'test' schema has many required fields which this two-column
        # CSV does not contain, so it should fail
        with makeNamedTemporaryCSV([
            [u'col1', u'col2'],
            [u'val1_1', u'val1_2'],
        ]) as filename:
            with self.assertRaises(ValueError):
                validate_header('test', filename)

    def test_validate_header_all_required_fields_populated(self):
        # regardless of the fact that these values shouldn't validate
        # for the fields, the header is correct and should validate just fine
        with makeNamedTemporaryCSV([
            [
                'internal_person_id',
                'internal_event_id',
                'location_id',
                'ssn',
                'birthdate',
                'full_name'
            ],
            [
                'val1_1',
                'val1_2',
                'val1_3',
                'val1_4',
                'val1_5',
                'val1_6',
            ],
        ]) as filename:
            validate_header('test', filename)

def test_write_match_log():
    with rig_test_client() as (app, engine):
        # engine = create_engine(postgresql.url())
        Base.metadata.create_all(engine)
        db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

        write_upload_log(
            db_session=db_session,
            upload_id="234",
            jurisdiction_slug="test",
            event_type_slug="hmis_service_stays",
            user_id=1,
            given_filename="hmis_test.csv",
            upload_start_time=datetime.now(),
            upload_complete_time=datetime.now(),
            upload_status=True,
            validate_start_time=datetime.now(),
            validate_complete_time=datetime.now(),
            validate_status=True,
            num_rows=1,
            file_size=1,
            file_hash="abcd",
            s3_upload_path="s3://somewhere"
        )
        match_start_timestamp = datetime.now()
        time.sleep(1)
        match_complete_timestamp = datetime.now()
        write_match_log(
            db_session=db_session,
            match_job_id="123",
            upload_id="234",
            match_start_at=match_start_timestamp,
            match_complete_at=match_complete_timestamp,
            match_status=True,
            match_runtime=match_complete_timestamp - match_start_timestamp
            )

        log = db_session.query(MatchLog).all()
        assert log[0].id == "123"
        assert log[0].upload_id == "234"
        assert log[0].match_start_timestamp == match_start_timestamp
        assert log[0].match_status == True
        assert log[0].runtime == match_complete_timestamp - match_start_timestamp

class WriteMatchesToDBTest(TestCase):
    def test_write_matches_to_db(self):
        BOOTSTRAPPED_HMIS_FILE = 'sample_data/matched/bootstrapped_hmis_data_20180401.csv'
        MATCHES_HMIS_FILE = 'sample_data/matched/matchesonly_hmis_data.csv'

        with testing.postgresql.Postgresql() as postgresql:
            db_engine = create_engine(postgresql.url())
            create_and_populate_matched_table(
                table_name='hmis_service_stays',
                db_engine=db_engine,
                file_path=BOOTSTRAPPED_HMIS_FILE
            )
            # generate expected matches by taking the first column of the matched id spreadsheet
            with open(MATCHES_HMIS_FILE, 'rb') as f:
                reader = unicodecsv.reader(f)
                next(reader)
                expected_matched_ids = set(row[0] for row in reader)

            # write these matches to the DB
            with open(MATCHES_HMIS_FILE, 'rb') as fh:
                write_matches_to_db(
                    db_engine=db_engine,
                    event_type='hmis_service_stays',
                    jurisdiction='boone',
                    matches_filehandle=fh
                )

            full_table_name = generate_matched_table_name('boone', 'hmis_service_stays')
            retrieved_matched_ids = set([row[0] for row in db_engine.execute('select distinct matched_id from {}'.format(full_table_name))])
            assert retrieved_matched_ids == expected_matched_ids
