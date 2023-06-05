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

import google.api_core.exceptions
import google.cloud.dlp_v2
import google.cloud.exceptions
import google.cloud.storage
import pytest

import stored_infotype

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
UNIQUE_STRING = str(uuid.uuid4()).split("-")[0]
TEST_BUCKET_NAME = GCLOUD_PROJECT + "-dlp-python-client-test" + UNIQUE_STRING
RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
RESOURCE_FILE_NAMES = ["term_list.txt"]
STORED_INFO_TYPE_ID = "github-usernames"

DLP_CLIENT = google.cloud.dlp_v2.DlpServiceClient()


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

    bucket.delete(force=True)


def delete_stored_info_type(out: str) -> None:
    for line in str(out).split("\n"):
        if "Updated stored infoType successfully" in line:
            stored_info_type_id = line.split(":")[1].strip()
            DLP_CLIENT.delete_stored_info_type(name=stored_info_type_id)


def test_create_and_update_stored_infotype(
    bucket: google.cloud.storage.bucket.Bucket, capsys: pytest.CaptureFixture
) -> None:
    out = ""
    try:
        stored_infotype.create_stored_infotype(
            GCLOUD_PROJECT,
            STORED_INFO_TYPE_ID,
            bucket.name,
        )
        out, _ = capsys.readouterr()
        assert STORED_INFO_TYPE_ID in out

        stored_info_type_id = str(out).split("\n")[0].split(":")[1].strip()

        stored_infotype.update_stored_infotype(
            GCLOUD_PROJECT,
            STORED_INFO_TYPE_ID,
            f"{bucket.name}/{RESOURCE_FILE_NAMES[0]}",
            f"{bucket.name}"
        )
        out, _ = capsys.readouterr()
        assert stored_info_type_id in out
    finally:
        delete_stored_info_type(out)
