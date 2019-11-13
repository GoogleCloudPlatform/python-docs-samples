import os

import decorator
import google.cloud.pubsub
import pytest
from google.api_core import exceptions

GCLOUD_PROJECT = os.getenv('GCLOUD_PROJECT')
TEST_BUCKET_NAME = GCLOUD_PROJECT + '-dlp-python-client-test'
SHOULD_PASS_VPCSC = os.getenv('SHOULD_PASS_VPCSC').lower() == "true"
VPC_FAILURE_MESSAGE = "Expected to fail if VPCSC is misconfigured."
RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'resources')
RESOURCE_FILE_NAMES = ['test.txt', 'test.png', 'harmless.txt', 'accounts.txt']

# VPCSC function wrappers.
##################################################
@pytest.mark.xfail
def is_rejected_by_vpc(call):
    try:
        call()
    except exceptions.PermissionDenied as e:
        return "Request is prohibited by organization's policy." in e.message
    except exceptions.Forbidden as e:
        return "Request violates VPC Service Controls." in e.message
    except:
        return False


def vpc_check(fn):
    def wrapped(fn, *args, **kwargs):
        if SHOULD_PASS_VPCSC:
            return fn(*args, **kwargs)
        else:
            def call(): return fn(*args, **kwargs)
            return is_rejected_by_vpc(call)
    return decorator.decorator(wrapped, fn)

# VPCSC fixture helpers.
##################################################
@pytest.fixture(scope='module')
def bucket():
    # Creates a GCS bucket, uploads files required for the test, and tears down
    # the entire bucket afterwards.
    client = google.cloud.storage.Client()
    try:
        bucket = client.get_bucket(TEST_BUCKET_NAME)
    except google.cloud.exceptions.NotFound:
        try:
            bucket = client.create_bucket(TEST_BUCKET_NAME)
        except google.api_core.exceptions.PermissionDenied as e:
            if "Request is prohibited by organization's policy." in e.message:
                pytest.skip(VPC_FAILURE_MESSAGE)
        except google.api_core.exceptions.Forbidden as e:
            if "Request violates VPC Service Controls." in e.message:
                pytest.skip(VPC_FAILURE_MESSAGE)

    # Upoad the blobs and keep track of them in a list.
    blobs = []
    for name in RESOURCE_FILE_NAMES:
        path = os.path.join(RESOURCE_DIRECTORY, name)
        blob = bucket.blob(name)
        blob.upload_from_filename(path)
        blobs.append(blob)

    # Yield the object to the test; lines after this execute as a teardown.
    yield bucket

    # Delete the files.
    for blob in blobs:
        try:
            blob.delete()
        except google.cloud.exceptions.NotFound:
            print('Issue during teardown, missing blob')

    # Attempt to delete the bucket; this will only work if it is empty.
    bucket.delete()
