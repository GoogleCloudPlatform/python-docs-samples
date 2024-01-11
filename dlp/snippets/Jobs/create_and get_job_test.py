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

import create_job
import delete_job
import get_job

import google.cloud.storage

import pytest

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
UNIQUE_STRING = str(uuid.uuid4()).split("-")[0]
TEST_BUCKET_NAME = GCLOUD_PROJECT + "-dlp-python-client-test" + UNIQUE_STRING
RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), "../resources")
RESOURCE_FILE_NAMES = ["test.txt", "test.png", "harmless.txt", "accounts.txt"]
test_job_id = f"test-job-{uuid.uuid4()}"


@pytest.fixture(scope="module")
def bucket() -> Iterator[google.cloud.storage.bucket.Bucket]:
    # Creates a GCS bucket, uploads files required for the test, and tears down
    # the entire bucket afterwards.

    client = google.cloud.storage.Client()
    try:
        bucket = client.get_bucket(TEST_BUCKET_NAME)
    except google.cloud.exceptions.NotFound:
        bucket = client.create_bucket(TEST_BUCKET_NAME)

    # Upload the blobs and keep track of them in a list.
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


def test_create_dlp_job(
    bucket: google.cloud.storage.bucket.Bucket, capsys: pytest.CaptureFixture
) -> None:
    create_job.create_dlp_job(
        GCLOUD_PROJECT,
        bucket.name,
        ["EMAIL_ADDRESS", "CREDIT_CARD_NUMBER"],
        job_id=test_job_id,
    )
    out, _ = capsys.readouterr()
    assert test_job_id in out

    job_name = f"i-{test_job_id}"

    get_job.get_dlp_job(GCLOUD_PROJECT, job_name)

    out, _ = capsys.readouterr()
    assert job_name in out

    delete_job.delete_dlp_job(GCLOUD_PROJECT, job_name)
