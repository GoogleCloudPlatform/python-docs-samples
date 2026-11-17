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

"""Integration tests that run the Cloud Scheduler job samples live.

These tests are skipped unless SERVICE_URL is set.

The Terraform fixture in .maintenance/fixtures/cloudscheduler_receiver
provisions the resources below; export its outputs as these variables.

Required environment variables:
    GOOGLE_CLOUD_PROJECT: Project that runs the tests. It must have an
        App Engine app in GOOGLE_CLOUD_LOCATION's region.
    SERVICE_URL: URL of the deployed cloud_scheduler/receiver Cloud Run function.

Optional environment variables:
    GOOGLE_CLOUD_LOCATION: Region for the jobs (default 'us-central1').
    SERVICE_ACCOUNT_EMAIL: Service account with the Cloud Run Invoker role on
        the receiver (default 'scheduler-invoker@PROJECT.iam.gserviceaccount.com').
    TOPIC_ID: Existing Pub/Sub topic (default 'scheduler-sample-topic').
"""

import os
import time
from typing import Callable, Iterator
import uuid

from google.api_core import exceptions
from google.api_core import retry
from google.cloud import scheduler_v1
import pytest

from .. import (
    create_appengine_job,
    create_http_job_oauth,
    create_job,
    create_job_with_retry,
    create_pubsub_job,
    delete_job,
    get_job,
    list_jobs,
    pause_job,
    resume_job,
    run_job,
    update_job,
)

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
LOCATION_ID = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
SERVICE_URL = os.environ.get("SERVICE_URL", "")
SERVICE_ACCOUNT_EMAIL = os.environ.get(
    "SERVICE_ACCOUNT_EMAIL",
    f"scheduler-invoker@{PROJECT_ID}.iam.gserviceaccount.com",
)
TOPIC_ID = os.environ.get("TOPIC_ID", "scheduler-sample-topic")

pytestmark = pytest.mark.skipif(
    not (PROJECT_ID and SERVICE_URL),
    reason="Set GOOGLE_CLOUD_PROJECT and SERVICE_URL to run integration tests.",
)

# Cloud Scheduler rejects a change to a job while a previous change is still
# being applied, with ABORTED: "sync mutate calls cannot be queued".
retry_aborted = retry.Retry(
    predicate=retry.if_exception_type(exceptions.Aborted), timeout=120
)


def run_sample(
    capsys: pytest.CaptureFixture[str], sample: Callable[..., None], *args: str
) -> str:
    """Runs a sample, retrying while the job has a change in progress."""
    for _ in range(10):
        sample(*args)
        out, err = capsys.readouterr()
        if "cannot be queued" not in err:
            assert "error:" not in err, err
            return out
        time.sleep(5)
    pytest.fail(f"{sample.__name__} kept failing with ABORTED")


@pytest.fixture(scope="module")
def client() -> scheduler_v1.CloudSchedulerClient:
    return scheduler_v1.CloudSchedulerClient()


def job_name(job_id: str) -> str:
    return f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/jobs/{job_id}"


@pytest.fixture
def job_id(client: scheduler_v1.CloudSchedulerClient) -> Iterator[str]:
    """Provides an unused job ID and deletes the job after the test."""
    job_id = f"test-job-{uuid.uuid4().hex[:12]}"
    yield job_id
    try:
        client.delete_job(name=job_name(job_id), retry=retry_aborted)
    except exceptions.NotFound:
        pass


@pytest.fixture
def existing_job_id(client: scheduler_v1.CloudSchedulerClient, job_id: str) -> str:
    """Creates an HTTP job that calls the receiver with an OIDC token."""
    assert SERVICE_URL, "Set SERVICE_URL to a deployed receiver service."
    client.create_job(
        parent=f"projects/{PROJECT_ID}/locations/{LOCATION_ID}",
        job=scheduler_v1.Job(
            name=job_name(job_id),
            http_target=scheduler_v1.HttpTarget(
                uri=SERVICE_URL,
                http_method=scheduler_v1.HttpMethod.POST,
                body=b"test-payload",
                oidc_token=scheduler_v1.OidcToken(
                    service_account_email=SERVICE_ACCOUNT_EMAIL,
                    audience=SERVICE_URL,
                ),
            ),
            schedule="0 9 * * 1",
            time_zone="UTC",
        ),
        retry=retry_aborted,
    )
    return job_id


def test_create_job(capsys: pytest.CaptureFixture[str], job_id: str) -> None:
    assert SERVICE_URL, "Set SERVICE_URL to a deployed receiver service."
    create_job.create_job(
        PROJECT_ID, LOCATION_ID, job_id, SERVICE_URL, SERVICE_ACCOUNT_EMAIL
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {job_name(job_id)}" in out
    assert "State: ENABLED" in out
    assert "Time Zone: UTC" in out
    assert "error:" not in err


def test_create_job_already_exists(
    capsys: pytest.CaptureFixture[str], existing_job_id: str
) -> None:
    create_job.create_job(
        PROJECT_ID, LOCATION_ID, existing_job_id, SERVICE_URL, SERVICE_ACCOUNT_EMAIL
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert f"error: job '{existing_job_id}' already exists" in err


def test_create_appengine_job(capsys: pytest.CaptureFixture[str], job_id: str) -> None:
    create_appengine_job.create_appengine_job(PROJECT_ID, LOCATION_ID, job_id)

    out, err = capsys.readouterr()
    assert f"Resource ID: {job_name(job_id)}" in out
    assert "State: ENABLED" in out
    assert "error:" not in err


def test_create_http_job_oauth(capsys: pytest.CaptureFixture[str], job_id: str) -> None:
    create_http_job_oauth.create_http_job_oauth(
        PROJECT_ID,
        LOCATION_ID,
        job_id,
        "example-workflow-template",
        SERVICE_ACCOUNT_EMAIL,
    )

    out, err = capsys.readouterr()
    expected_uri = (
        f"https://dataproc.googleapis.com/v1/projects/{PROJECT_ID}/regions/"
        f"{LOCATION_ID}/workflowTemplates/example-workflow-template:instantiate"
    )
    assert f"Resource ID: {job_name(job_id)}" in out
    assert f"Target URI: {expected_uri}\n" in out
    assert "error:" not in err


def test_create_pubsub_job(capsys: pytest.CaptureFixture[str], job_id: str) -> None:
    create_pubsub_job.create_pubsub_job(PROJECT_ID, LOCATION_ID, job_id, TOPIC_ID)

    out, err = capsys.readouterr()
    assert f"Resource ID: {job_name(job_id)}" in out
    assert f"Topic: projects/{PROJECT_ID}/topics/{TOPIC_ID}" in out
    assert "error:" not in err


def test_create_job_with_retry(capsys: pytest.CaptureFixture[str], job_id: str) -> None:
    assert SERVICE_URL, "Set SERVICE_URL to a deployed receiver service."
    create_job_with_retry.create_job_with_retry(
        PROJECT_ID, LOCATION_ID, job_id, SERVICE_URL, SERVICE_ACCOUNT_EMAIL
    )

    out, err = capsys.readouterr()
    assert f"Resource ID: {job_name(job_id)}" in out
    assert "Retry Count: 3" in out
    assert "Max Retry Duration: 1:00:00" in out
    assert "error:" not in err


def test_job_lifecycle(
    capsys: pytest.CaptureFixture[str], existing_job_id: str
) -> None:
    args = (PROJECT_ID, LOCATION_ID, existing_job_id)

    assert "State: PAUSED" in run_sample(capsys, pause_job.pause_job, *args)
    assert "State: PAUSED" in run_sample(capsys, get_job.get_job, *args)
    assert "State: ENABLED" in run_sample(capsys, resume_job.resume_job, *args)
    out = run_sample(capsys, update_job.update_job, *args)
    assert "Schedule: 0 10 * * 1-5" in out
    out = run_sample(capsys, list_jobs.list_jobs, PROJECT_ID, LOCATION_ID)
    assert f"Resource ID: {job_name(existing_job_id)}" in out
    assert "State: DELETED" in run_sample(capsys, delete_job.delete_job, *args)


def test_run_job_reaches_receiver(
    capsys: pytest.CaptureFixture[str],
    client: scheduler_v1.CloudSchedulerClient,
    existing_job_id: str,
) -> None:
    run_job.run_job(PROJECT_ID, LOCATION_ID, existing_job_id)
    out, err = capsys.readouterr()
    assert f"Resource ID: {job_name(existing_job_id)}" in out
    assert "error:" not in err

    # The run is asynchronous. Wait for the receiver to accept the request,
    # which confirms that the Cloud Run function accepted the job's OIDC token.
    deadline = time.monotonic() + 300
    job = client.get_job(name=job_name(existing_job_id))
    while time.monotonic() < deadline and not job.last_attempt_time:
        time.sleep(5)
        job = client.get_job(name=job_name(existing_job_id))
    assert job.last_attempt_time, "The job didn't run within 5 minutes."
    assert job.status.code == 0, job.status.message

    out = run_sample(capsys, get_job.get_job, PROJECT_ID, LOCATION_ID, existing_job_id)
    assert "Status Code: 0" in out


def test_job_not_found(capsys: pytest.CaptureFixture[str], job_id: str) -> None:
    for sample in (get_job.get_job, pause_job.pause_job, delete_job.delete_job):
        sample(PROJECT_ID, LOCATION_ID, job_id)
        out, err = capsys.readouterr()
        assert out == ""
        assert f"error: job '{job_id}' not found" in err
