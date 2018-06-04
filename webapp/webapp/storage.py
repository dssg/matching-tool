import s3fs
from urllib.parse import urlparse
from contextlib import contextmanager


@contextmanager
def open_sesame(path, *args, **kwargs):
    """Opens files either on s3 or a filesystem according to the path's scheme

    Uses s3fs so boto3 is used.
    This means mock_s3 can be used for tests, instead of the mock_s3_deprecated
    """
    path_parsed = urlparse(path)
    scheme = path_parsed.scheme  # If '' of 'file' is a regular file or 's3'

    if not scheme or scheme == 'file':  # Local file
        with open(path, *args, **kwargs) as f:
            yield f
    elif scheme == 's3':
        s3 = s3fs.S3FileSystem()
        with s3.open(path, *args, **kwargs) as f:
            yield f
