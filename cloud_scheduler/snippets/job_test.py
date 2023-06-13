# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid

from google.api_core import exceptions
from google.cloud import scheduler_v1

import pytest

import create_job
import delete_job

TEST_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
TEST_LOCATION = os.getenv("LOCATION_ID", "us-central1")
TEST_JOB_ID = f"my-job-{uuid.uuid4().hex}"


def test_create_job() -> None:
    client = scheduler_v1.CloudSchedulerClient()

    job = create_job.create_scheduler_job(TEST_PROJECT_ID, TEST_LOCATION, "my-service")
    assert job.name.startswith(
        client.common_location_path(TEST_PROJECT_ID, TEST_LOCATION)
    )

    client.delete_job(scheduler_v1.DeleteJobRequest(name=job.name))


def test_delete_job() -> None:
    client = scheduler_v1.CloudSchedulerClient()

    client.create_job(
        scheduler_v1.CreateJobRequest(
            parent=client.common_location_path(TEST_PROJECT_ID, TEST_LOCATION),
            job=scheduler_v1.Job(
                name=client.job_path(TEST_PROJECT_ID, TEST_LOCATION, TEST_JOB_ID),
                app_engine_http_target=scheduler_v1.AppEngineHttpTarget(
                    app_engine_routing=scheduler_v1.AppEngineRouting(
                        service="service-id"
                    ),
                    relative_uri="/log_payload",
                    http_method=scheduler_v1.HttpMethod.POST,
                    body=b"Hello World",
                ),
                schedule="* * * * *",
                time_zone="America/Los_Angeles",
            ),
        )
    )

    # Deleting an existant job succeeds
    delete_job.delete_scheduler_job(TEST_PROJECT_ID, TEST_LOCATION, TEST_JOB_ID)

    # Deleting a non-existant job fails with a not found error
    with pytest.raises(exceptions.NotFound):
        delete_job.delete_scheduler_job(TEST_PROJECT_ID, TEST_LOCATION, TEST_JOB_ID)
