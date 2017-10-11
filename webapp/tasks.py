from smart_open import smart_open
from datetime import date, datetime
from webapp.models import Upload
from hashlib import md5
import os


def upload_to_s3(
    path_template,
    service_provider,
    jurisdiction,
    upload_id,
    local_filename
):
    datestring = date.today().isoformat()
    full_s3_path = path_template\
        .replace('{service_provider}', service_provider)\
        .replace('{jurisdiction}', jurisdiction)\
        .replace('{date}', datestring)\
        .replace('{upload_id}', upload_id)
    with smart_open(local_filename) as infile:
        with smart_open(full_s3_path, 'w') as outfile:
            outfile.write(infile.read())


def sync_upload_metadata(
    upload_id,
    service_provider,
    jurisdiction,
    user,
    given_filename,
    local_filename,
    db_session
):
    with smart_open(local_filename, 'rb') as infile:
        num_rows = sum(1 for _ in infile)
        infile.seek(0)
        file_size = os.fstat(infile.fileno()).st_size
        file_hash = md5(infile.read()).hexdigest()

        db_object = Upload(
            id=upload_id,
            jurisdiction_slug=jurisdiction,
            service_provider_slug=service_provider,
            user_id=user.id,
            given_filename=given_filename,
            upload_timestamp=datetime.today(),
            num_rows=num_rows,
            file_size=file_size,
            file_hash=file_hash
        )
        db_session.add(db_object)
        db_session.commit()
