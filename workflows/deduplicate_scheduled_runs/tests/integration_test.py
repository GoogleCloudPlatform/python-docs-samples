# Copyright 2026 Google LLC
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

"""Integration test: Cloud Scheduler → this function → a workflow execution.

Skipped unless RUN_INTEGRATION_TESTS is "true". Needs the function (main.py)
and a target workflow deployed, and:
    GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION (default 'us-central1'),
    FUNCTION_URL, SERVICE_ACCOUNT_EMAIL, WORKFLOW_ID, and FIRESTORE_DATABASE.

A forced run sends the job's next scheduled time, so forcing the same job twice
delivers the same scheduled run twice.
"""

import json
import os
import time
from typing import Iterator
import uuid

from google.api_core import exceptions
from google.api_core import retry
from google.cloud import scheduler_v1
from google.cloud.workflows import executions_v1
import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_INTEGRATION_TESTS") != "true",
    reason="Set RUN_INTEGRATION_TESTS=true to run integration tests.",
)

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
LOCATION_ID = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
FUNCTION_URL = os.environ.get("FUNCTION_URL", "")
SERVICE_ACCOUNT_EMAIL = os.environ.get("SERVICE_ACCOUNT_EMAIL", "")
WORKFLOW_ID = os.environ.get("WORKFLOW_ID", "")

# Cloud Scheduler rejects a change to a job while another change is in progress.
retry_aborted = retry.Retry(
    predicate=retry.if_exception_type(exceptions.Aborted), timeout=120
)


@pytest.fixture
def job_name() -> Iterator[str]:
    """Creates a Scheduler job that calls the function, and deletes it afterward."""
    client = scheduler_v1.CloudSchedulerClient()
    parent = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}"
    name = f"{parent}/jobs/test-job-{uuid.uuid4().hex[:12]}"
    client.create_job(
        parent=parent,
        job=scheduler_v1.Job(
            name=name,
            http_target=scheduler_v1.HttpTarget(
                uri=FUNCTION_URL,
                http_method=scheduler_v1.HttpMethod.POST,
                oidc_token=scheduler_v1.OidcToken(
                    service_account_email=SERVICE_ACCOUNT_EMAIL,
                    audience=FUNCTION_URL,
                ),
            ),
            schedule="0 9 * * 1",
            time_zone="UTC",
        ),
        retry=retry_aborted,
    )
    yield name
    client.delete_job(name=name, retry=retry_aborted)


def executions_for(job_id: str) -> list[executions_v1.Execution]:
    client = executions_v1.ExecutionsClient()
    request = executions_v1.ListExecutionsRequest(
        parent=f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/workflows/{WORKFLOW_ID}",
        view=executions_v1.ExecutionView.FULL,
    )
    executions = []
    for execution in client.list_executions(request=request):
        try:
            args = json.loads(execution.argument or "{}")
        except json.JSONDecodeError:
            continue
        if isinstance(args, dict) and args.get("job_name") == job_id:
            executions.append(execution)
    return executions


def test_duplicate_delivery_starts_one_execution(job_name: str) -> None:
    client = scheduler_v1.CloudSchedulerClient()
    job_id = job_name.rsplit("/", 1)[-1]

    client.run_job(name=job_name, retry=retry_aborted)
    deadline = time.monotonic() + 300
    while not executions_for(job_id):
        assert time.monotonic() < deadline, "The workflow didn't start."
        time.sleep(10)

    # Force the same job again: it delivers the same scheduled run.
    client.run_job(name=job_name, retry=retry_aborted)
    deadline = time.monotonic() + 300
    job = client.get_job(name=job_name)
    first_attempt = job.last_attempt_time
    while job.last_attempt_time == first_attempt:
        assert time.monotonic() < deadline, "The second delivery didn't happen."
        time.sleep(10)
        job = client.get_job(name=job_name)

    assert job.status.code == 0, job.status.message
    executions = executions_for(job_id)
    assert len(executions) == 1
    argument = json.loads(executions[0].argument)
    assert argument["scheduled_minute"]
