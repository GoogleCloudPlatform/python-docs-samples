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

import google.cloud.dlp

import list_jobs as jobs

import pytest


GCLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
TEST_COLUMN_NAME = "zip_code"
TEST_TABLE_PROJECT_ID = "bigquery-public-data"
TEST_DATASET_ID = "san_francisco"
TEST_TABLE_ID = "bikeshare_trips"
UNIQUE_STRING = str(uuid.uuid4()).split("-")[0]
test_job_id = f"test-job-{uuid.uuid4()}"


@pytest.fixture(scope="module")
def test_job_name() -> Iterator[str]:
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


def test_list_dlp_jobs(test_job_name: str, capsys: pytest.CaptureFixture) -> None:
    jobs.list_dlp_jobs(GCLOUD_PROJECT)

    out, _ = capsys.readouterr()
    assert test_job_name not in out


def test_list_dlp_jobs_with_filter(
    test_job_name: str, capsys: pytest.CaptureFixture
) -> None:
    jobs.list_dlp_jobs(
        GCLOUD_PROJECT,
        filter_string="state=RUNNING OR state=DONE",
        job_type="RISK_ANALYSIS_JOB",
    )

    out, _ = capsys.readouterr()
    assert test_job_name in out


def test_list_dlp_jobs_with_job_type(
    test_job_name: str, capsys: pytest.CaptureFixture
) -> None:
    jobs.list_dlp_jobs(GCLOUD_PROJECT, job_type="INSPECT_JOB")

    out, _ = capsys.readouterr()
    assert test_job_name not in out  # job created is a risk analysis job
