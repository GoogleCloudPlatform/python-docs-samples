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
import uuid

import google.cloud.storage
import pytest

import jobs

GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
TEST_COLUMN_NAME = "zip_code"
TEST_TABLE_PROJECT_ID = "bigquery-public-data"
TEST_DATASET_ID = "san_francisco"
TEST_TABLE_ID = "bikeshare_trips"
UNIQUE_STRING = str(uuid.uuid4()).split("-")[0]
TEST_BUCKET_NAME = GCLOUD_PROJECT + "-dlp-python-client-test" + UNIQUE_STRING
RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
RESOURCE_FILE_NAMES = ["test.txt", "test.png", "harmless.txt", "accounts.txt"]
test_job_id = f"test-job-{uuid.uuid4()}"


@pytest.fixture(scope="module")
def bucket():
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


@pytest.fixture(scope="module")
def test_job_name():
    import google.cloud.dlp

    dlp = google.cloud.dlp_v2.DlpServiceClient()

    parent = f"projects/{GCLOUD_PROJECT}"

    # Construct job request
    risk_job = {
        "privacy_metric": {
            "categorical_stats_config": {"field": {"name": TEST_COLUMN_NAME}}
        },
        "source_table": {
            "project_id": TEST_TABLE_PROJECT_ID,
            "dataset_id": TEST_DATASET_ID,
            "table_id": TEST_TABLE_ID,
        },
    }

    response = dlp.create_dlp_job(
        request={"parent": parent, "risk_job": risk_job, "job_id": test_job_id}
    )
    full_path = response.name
    # API expects only job name, not full project path
    job_name = full_path[full_path.rfind("/") + 1 :]
    yield job_name

    # clean up job if not deleted
    try:
        dlp.delete_dlp_job(request={"name": full_path})
    except google.api_core.exceptions.NotFound:
        print("Issue during teardown, missing job")


def test_list_dlp_jobs(test_job_name, capsys):
    jobs.list_dlp_jobs(GCLOUD_PROJECT)

    out, _ = capsys.readouterr()
    assert test_job_name not in out


def test_list_dlp_jobs_with_filter(test_job_name, capsys):
    jobs.list_dlp_jobs(
        GCLOUD_PROJECT,
        filter_string="state=RUNNING OR state=DONE",
        job_type="RISK_ANALYSIS_JOB",
    )

    out, _ = capsys.readouterr()
    assert test_job_name in out


def test_list_dlp_jobs_with_job_type(test_job_name, capsys):
    jobs.list_dlp_jobs(GCLOUD_PROJECT, job_type="INSPECT_JOB")

    out, _ = capsys.readouterr()
    assert test_job_name not in out  # job created is a risk analysis job


def test_delete_dlp_job(test_job_name, capsys):
    jobs.delete_dlp_job(GCLOUD_PROJECT, test_job_name)


def test_create_dlp_job(bucket, capsys):
    jobs.create_dlp_job(
        GCLOUD_PROJECT,
        bucket.name,
        ["EMAIL_ADDRESS", "CREDIT_CARD_NUMBER"],
        job_id=test_job_id,
    )
    out, _ = capsys.readouterr()
    assert test_job_id in out

    job_name = f"i-{test_job_id}"
    jobs.delete_dlp_job(GCLOUD_PROJECT, job_name)
