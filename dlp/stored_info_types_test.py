# Copyright 2017 Google Inc.
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

import os

import google.api_core.exceptions
import google.cloud.storage

import pytest

import stored_info_types


GCLOUD_PROJECT = os.getenv('GCLOUD_PROJECT')
TEST_BUCKET_NAME = GCLOUD_PROJECT + '-dlp-python-client-test'
RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'resources')
RESOURCE_FILE_NAMES = [
    'test.txt', 'test.png', 'harmless.txt', 'accounts.txt', 'dictionary.txt'
]
TEST_STORED_INFO_TYPE_ID = 'test-stored-info-type'


@pytest.fixture(scope='module')
def bucket():
    # Creates a GCS bucket, uploads files required for the test, and tears down
    # the entire bucket afterwards.

    client = google.cloud.storage.Client()
    try:
        bucket = client.get_bucket(TEST_BUCKET_NAME)
    except google.cloud.exceptions.NotFound:
        bucket = client.create_bucket(TEST_BUCKET_NAME)

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
        blob.delete()

    # Attempt to delete the bucket; this will only work if it is empty.
    bucket.delete()


def test_create_list_and_delete_stored_info_type(bucket, capsys):
    try:
        gcs_input_file_path = 'gs://{}/dictionary.txt'.format(bucket.name)
        gcs_output_path = 'gs://{}/'.format(bucket.name)
        stored_info_types.create_stored_info_type_from_gcs_files(
            GCLOUD_PROJECT, gcs_input_file_path, gcs_output_path,
            stored_info_type_id=TEST_STORED_INFO_TYPE_ID,
        )

    except google.api_core.exceptions.InvalidArgument:
        # Stored infoType already exists, perhaps due to a previous test.
        stored_info_types.delete_stored_info_type(
            GCLOUD_PROJECT, TEST_STORED_INFO_TYPE_ID)

        out, _ = capsys.readouterr()
        assert TEST_STORED_INFO_TYPE_ID in out

        # Try again and move on.
        stored_info_types.create_stored_info_type_from_gcs_files(
            GCLOUD_PROJECT, gcs_input_file_path, gcs_output_path,
            stored_info_type_id=TEST_STORED_INFO_TYPE_ID,
        )

    out, _ = capsys.readouterr()
    assert TEST_STORED_INFO_TYPE_ID in out

    stored_info_types.list_stored_info_types(GCLOUD_PROJECT)

    out, _ = capsys.readouterr()
    assert TEST_STORED_INFO_TYPE_ID in out

    stored_info_types.delete_stored_info_type(
        GCLOUD_PROJECT, TEST_STORED_INFO_TYPE_ID)

    out, _ = capsys.readouterr()
    assert TEST_STORED_INFO_TYPE_ID in out
