#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import uuid

from flaky import flaky

import google.auth
from google.cloud import batch_v1
from google.cloud import storage
import pytest

from .test_basics import _test_body
from ..create.create_with_mounted_bucket import create_script_job_with_bucket

PROJECT = google.auth.default()[1]
REGION = 'europe-north1'

TIMEOUT = 600  # 10 minutes

WAIT_STATES = {
    batch_v1.JobStatus.State.STATE_UNSPECIFIED,
    batch_v1.JobStatus.State.QUEUED,
    batch_v1.JobStatus.State.RUNNING,
    batch_v1.JobStatus.State.SCHEDULED,
}


@pytest.fixture
def job_name():
    return f"test-job-{uuid.uuid4().hex[:10]}"


@pytest.fixture()
def test_bucket():
    bucket_name = f"test-bucket-{uuid.uuid4().hex[:8]}"
    client = storage.Client()
    client.create_bucket(bucket_name, location="eu")

    yield bucket_name

    bucket = client.get_bucket(bucket_name)
    bucket.delete(force=True)


def _test_bucket_content(test_bucket):
    client = storage.Client()
    bucket = client.get_bucket(test_bucket)

    file_name_template = "output_task_{task_number}.txt"
    file_content_template = "Hello world from task {task_number}.\n"

    for i in range(4):
        blob = bucket.blob(file_name_template.format(task_number=i))
        content = blob.download_as_bytes().decode()
        assert content == file_content_template.format(task_number=i)


@flaky(max_runs=3, min_passes=1)
def test_bucket_job(job_name, test_bucket):
    job = create_script_job_with_bucket(PROJECT, REGION, job_name, test_bucket)
    _test_body(job, lambda: _test_bucket_content(test_bucket))
