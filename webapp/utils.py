from uuid import uuid4

import csv
import tempfile

from contextlib import contextmanager


def unique_upload_id():
    return str(uuid4())


@contextmanager
def makeNamedTemporaryCSV(content, separator='|'):
    tf = tempfile.NamedTemporaryFile(delete=False)
    with open(tf.name, 'w') as write_stream:
        writer = csv.writer(write_stream, delimiter=separator)
        for row in content:
            writer.writerow(row)

    yield tf.name

    tf.close()
