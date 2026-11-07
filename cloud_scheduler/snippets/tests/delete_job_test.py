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

from .. import delete_job

PROJECT_ID = "test-project"
LOCATION_ID = "us-central1"
JOB_ID = "test-job"
PARENT = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}"
JOB_NAME = f"{PARENT}/jobs/{JOB_ID}"
CLIENT = "google.cloud.scheduler_v1.CloudSchedulerClient"


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
def test_delete_job_success(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.delete_job.return_value = None

    delete_job.delete_job(PROJECT_ID, LOCATION_ID, JOB_ID)

    request = client.delete_job.call_args.kwargs["request"]
    assert request.name == JOB_NAME
    out, err = capsys.readouterr()
    assert f"Resource ID: {JOB_NAME}" in out
    assert "State: DELETED" in out
    assert err == ""


@mock.patch(CLIENT)
def test_delete_job_not_found(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.delete_job.side_effect = exceptions.NotFound("test error detail")

    delete_job.delete_job(PROJECT_ID, LOCATION_ID, JOB_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith("error: job 'test-job' not found")
    assert "test error detail" in err


@mock.patch(CLIENT)
def test_delete_job_api_error(
    mock_client_class: mock.MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    client = mock_client_class.return_value
    client.delete_job.side_effect = exceptions.PermissionDenied("denied")

    delete_job.delete_job(PROJECT_ID, LOCATION_ID, JOB_ID)

    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith("error: failed to delete job")
    assert "denied" in err
