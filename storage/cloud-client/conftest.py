import os
import time
import uuid

from google.cloud import storage
import pytest


@pytest.fixture(scope="function")
def bucket():
    """Yields a bucket that is deleted after the test completes."""
    # The new projects enforces uniform bucket level access, so
    # we need to use the old main project for now.
    original_value = os.environ['GOOGLE_CLOUD_PROJECT']
    os.environ['GOOGLE_CLOUD_PROJECT'] = os.environ['MAIN_GOOGLE_CLOUD_PROJECT']
    bucket = None
    while bucket is None or bucket.exists():
        bucket_name = "uniform-bucket-level-access-{}".format(uuid.uuid4().hex)
        bucket = storage.Client().bucket(bucket_name)
    bucket.create()
    yield bucket
    time.sleep(3)
    bucket.delete(force=True)
    # Set the value back.
    os.environ['GOOGLE_CLOUD_PROJECT'] = original_value
