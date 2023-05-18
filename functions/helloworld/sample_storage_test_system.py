# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_storage_system_test]
from datetime import datetime
from os import getenv, path
import subprocess
import time
import uuid

from google.cloud import storage
import pytest

PROJECT = getenv('GCP_PROJECT')
BUCKET = getenv('BUCKET')

assert PROJECT is not None
assert BUCKET is not None


@pytest.fixture(scope='module')
def storage_client():
    yield storage.Client()


@pytest.fixture(scope='module')
def bucket_object(storage_client):
    bucket_object = storage_client.get_bucket(BUCKET)
    yield bucket_object


@pytest.fixture(scope='module')
def uploaded_file(bucket_object):
    name = f'test-{str(uuid.uuid4())}.txt'
    blob = bucket_object.blob(name)

    test_dir = path.dirname(path.abspath(__file__))
    blob.upload_from_filename(path.join(test_dir, 'test.txt'))
    yield name
    blob.delete()


def test_hello_gcs(uploaded_file):
    start_time = datetime.utcnow().isoformat()
    time.sleep(10)  # Wait for logs to become consistent

    log_process = subprocess.Popen([
        'gcloud',
        'alpha',
        'functions',
        'logs',
        'read',
        'hello_gcs_generic',
        '--start-time',
        start_time
    ], stdout=subprocess.PIPE)
    logs = str(log_process.communicate()[0])
    assert uploaded_file in logs
# [END functions_storage_system_test]
