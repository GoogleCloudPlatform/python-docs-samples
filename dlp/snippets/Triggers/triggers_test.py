# Copyright 2023 Google LLC
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
from typing import Iterator
import uuid

import create_trigger as ct
import delete_trigger as dt

import google.api_core.exceptions
import google.cloud.storage

import list_triggers as lt

import pytest

import update_trigger as ut

UNIQUE_STRING = str(uuid.uuid4()).split("-")[0]
GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
TEST_BUCKET_NAME = GCLOUD_PROJECT + "-dlp-python-client-test" + UNIQUE_STRING
RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), "../resources")
RESOURCE_FILE_NAMES = ["test.txt", "test.png", "harmless.txt", "accounts.txt"]
TEST_TRIGGER_ID = "test-trigger" + UNIQUE_STRING


@pytest.fixture(scope="module")
def bucket() -> Iterator[google.cloud.storage.bucket.Bucket]:
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
        try:
            blob.delete()
        except google.cloud.exceptions.NotFound:
            print("Issue during teardown, missing blob")

    # Attempt to delete the bucket; this will only work if it is empty.
    bucket.delete()


def test_create_list_update_and_delete_trigger(
    bucket: google.cloud.storage.bucket.Bucket, capsys: pytest.CaptureFixture
) -> None:
    try:
        ct.create_trigger(
            GCLOUD_PROJECT,
            bucket.name,
            7,
            ["FIRST_NAME", "EMAIL_ADDRESS", "PHONE_NUMBER"],
            trigger_id=TEST_TRIGGER_ID,
        )
    except google.api_core.exceptions.InvalidArgument:
        # Trigger already exists, perhaps due to a previous interrupted test.
        dt.delete_trigger(GCLOUD_PROJECT, TEST_TRIGGER_ID)

        out, _ = capsys.readouterr()
        assert TEST_TRIGGER_ID in out

        # Try again and move on.
        ct.create_trigger(
            GCLOUD_PROJECT,
            bucket.name,
            7,
            ["FIRST_NAME", "EMAIL_ADDRESS", "PHONE_NUMBER"],
            trigger_id=TEST_TRIGGER_ID,
            auto_populate_timespan=True,
        )

    out, _ = capsys.readouterr()
    assert TEST_TRIGGER_ID in out

    lt.list_triggers(GCLOUD_PROJECT)

    out, _ = capsys.readouterr()
    assert TEST_TRIGGER_ID in out

    ut.update_trigger(
        GCLOUD_PROJECT,
        ["US_INDIVIDUAL_TAXPAYER_IDENTIFICATION_NUMBER"],
        TEST_TRIGGER_ID,
    )

    out, _ = capsys.readouterr()
    assert TEST_TRIGGER_ID in out
    assert "US_INDIVIDUAL_TAXPAYER_IDENTIFICATION_NUMBER" in out

    dt.delete_trigger(GCLOUD_PROJECT, TEST_TRIGGER_ID)

    out, _ = capsys.readouterr()
    assert TEST_TRIGGER_ID in out
