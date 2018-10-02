import os
from os.path import dirname
import s3fs
from urllib.parse import urlparse
from contextlib import contextmanager
from retrying import retry
import shutil
import logging
from pathlib import Path


@retry(stop_max_delay=15000, wait_fixed=3000)
@contextmanager
def open_sesame(path, *args, **kwargs):
    """Opens files either on s3 or a filesystem according to the path's scheme

    Uses s3fs so boto3 is used.
    This means mock_s3 can be used for tests, instead of the mock_s3_deprecated
    """
    path_parsed = urlparse(path)
    scheme = path_parsed.scheme  # If '' or 'file' then a regular file; if 's3' then 's3'

    if not scheme or scheme == 'file':  # Local file
        os.makedirs(dirname(path), exist_ok=True)
        with open(path, *args, **kwargs) as f:
            yield f
    elif scheme == 's3':
        s3 = s3fs.S3FileSystem()
        with s3.open(path, *args, **kwargs) as f:
            yield f


def remove_recursively(path):
    path_parsed = urlparse(path)
    scheme = path_parsed.scheme  # If '' or 'file' then a regular file; if 's3' then 's3'

    if not scheme or scheme == 'file':  # Local file
        if Path(path).exists():
            shutil.rmtree(path)
        else:
            logging.info('Path %s did not exist, so no removal attempted', path)
    elif scheme == 's3':
        s3 = s3fs.S3FileSystem()
        if s3.exists(path):
            s3.rm(path, recursive=True)
        else:
            logging.info('Path %s did not exist, so no removal attempted', path)
