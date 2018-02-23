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

import google.cloud.exceptions
import google.cloud.storage

import pytest

import inspect_content


GCLOUD_PROJECT = os.getenv('GCLOUD_PROJECT')
TEST_BUCKET_NAME = GCLOUD_PROJECT + '-dlp-python-client-test'
RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'resources')
RESOURCE_FILE_NAMES = ['test.txt', 'test.png', 'harmless.txt', 'accounts.txt']


@pytest.fixture(scope='module')
def bucket(request):
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


def test_inspect_string(capsys):
    test_string = 'I am Gary and my email is gary@example.com'

    inspect_content.inspect_string(
        test_string, include_quote=True)

    out, _ = capsys.readouterr()
    assert 'Info type: EMAIL_ADDRESS' in out


def test_inspect_string_with_info_types(capsys):
    test_string = 'I am Gary and my email is gary@example.com'

    inspect_content.inspect_string(
        test_string, info_types=['US_MALE_NAME'], include_quote=True)

    out, _ = capsys.readouterr()
    assert 'Info type: US_MALE_NAME' in out
    assert 'Info type: EMAIL_ADDRESS' not in out


def test_inspect_string_no_results(capsys):
    test_string = 'Nothing to see here'

    inspect_content.inspect_string(
        test_string, include_quote=True)

    out, _ = capsys.readouterr()
    assert 'No findings' in out


def test_inspect_file(capsys):
    test_filepath = os.path.join(RESOURCE_DIRECTORY, 'test.txt')

    inspect_content.inspect_file(
        test_filepath, include_quote=True)

    out, _ = capsys.readouterr()
    assert 'Info type: EMAIL_ADDRESS' in out


def test_inspect_file_with_info_types(capsys):
    test_filepath = os.path.join(RESOURCE_DIRECTORY, 'test.txt')

    inspect_content.inspect_file(
        test_filepath, ['PHONE_NUMBER'], include_quote=True)

    out, _ = capsys.readouterr()
    assert 'Info type: PHONE_NUMBER' in out
    assert 'Info type: EMAIL_ADDRESS' not in out


def test_inspect_file_no_results(capsys):
    test_filepath = os.path.join(RESOURCE_DIRECTORY, 'harmless.txt')

    inspect_content.inspect_file(
        test_filepath, include_quote=True)

    out, _ = capsys.readouterr()
    assert 'No findings' in out


def test_inspect_image_file(capsys):
    test_filepath = os.path.join(RESOURCE_DIRECTORY, 'test.png')

    inspect_content.inspect_file(
        test_filepath, include_quote=True)

    out, _ = capsys.readouterr()
    assert 'Info type: PHONE_NUMBER' in out


def test_inspect_gcs_file(bucket, capsys):
    inspect_content.inspect_gcs_file(bucket.name, 'test.txt')

    out, _ = capsys.readouterr()
    assert 'Info type: EMAIL_ADDRESS' in out


def test_inspect_gcs_file_with_info_types(bucket, capsys):
    inspect_content.inspect_gcs_file(
        bucket.name, 'test.txt', info_types=['EMAIL_ADDRESS'])

    out, _ = capsys.readouterr()
    assert 'Info type: EMAIL_ADDRESS' in out


def test_inspect_gcs_file_no_results(bucket, capsys):
    inspect_content.inspect_gcs_file(bucket.name, 'harmless.txt')

    out, _ = capsys.readouterr()
    assert 'No findings' in out


def test_inspect_gcs_image_file(bucket, capsys):
    inspect_content.inspect_gcs_file(bucket.name, 'test.png')

    out, _ = capsys.readouterr()
    assert 'Info type: EMAIL_ADDRESS' in out


def test_inspect_gcs_multiple_files(bucket, capsys):
    inspect_content.inspect_gcs_file(bucket.name, '*')

    out, _ = capsys.readouterr()
    assert 'Info type: PHONE_NUMBER' in out
    assert 'Info type: CREDIT_CARD' in out
