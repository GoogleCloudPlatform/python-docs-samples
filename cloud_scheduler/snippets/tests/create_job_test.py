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

from unittest import mock

from google.api_core import exceptions
from google.cloud import scheduler_v1
import pytest

from .. import create_job

PROJECT_ID = "test-project"
LOCATION_ID = "us-central1"
JOB_ID = "test-job"
PARENT = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}"
JOB_NAME = f"{PARENT}/jobs/{JOB_ID}"
CLIENT = "google.cloud.scheduler_v1.CloudSchedulerClient"
SERVICE_URL = "https://test-service.a.run.app/"
SERVICE_ACCOUNT_EMAIL = "invoker@test-project.iam.gserviceaccount.com"


def _job(**fields: object) -> scheduler_v1.Job:
    """Returns a job response, with defaults that fields can override."""
    job_fields: dict[str, object] = {
        "name": JOB_NAME,
        "schedule": "0 9 * * 1",
        "time_zone": "UTC",
        "state": scheduler_v1.Job.State.ENABLED,
    }
    job_fields.update(fields)
    return scheduler_v1.Job(**job_fields)


@mock.patch(CLIENT)
def test_create_job_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.create_job.return_value = _job()

    create_job.create_job(
        PROJECT_ID, LOCATION_ID, JOB_ID, SERVICE_URL, SERVICE_ACCOUNT_EMAIL
    )

    request = client.create_job.call_args.kwargs["request"]
    assert request.parent == PARENT
    assert request.job.name == JOB_NAME
    assert request.job.http_target.uri == SERVICE_URL
    assert request.job.http_target.http_method == scheduler_v1.HttpMethod.POST
    oidc_token = request.job.http_target.oidc_token
    assert oidc_token.service_account_email == SERVICE_ACCOUNT_EMAIL
    assert oidc_token.audience == SERVICE_URL
    assert request.job.time_zone == "UTC"
    assert request.job.attempt_deadline.total_seconds() == 300
    out, err = capsys.readouterr()
    assert f"Resource ID: {JOB_NAME}" in out
    assert "State: ENABLED" in out
    assert "Time Zone: UTC" in out
    assert err == ""


@mock.patch(CLIENT)
def test_create_job_already_exists(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.create_job.side_effect = exceptions.AlreadyExists("test error detail")

    create_job.create_job(
        PROJECT_ID, LOCATION_ID, JOB_ID, SERVICE_URL, SERVICE_ACCOUNT_EMAIL
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith("error: job 'test-job' already exists")
    assert "test error detail" in err


@mock.patch(CLIENT)
def test_create_job_api_error(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.create_job.side_effect = exceptions.PermissionDenied("denied")

    create_job.create_job(
        PROJECT_ID, LOCATION_ID, JOB_ID, SERVICE_URL, SERVICE_ACCOUNT_EMAIL
    )

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith("error: failed to create job")
    assert "denied" in err
