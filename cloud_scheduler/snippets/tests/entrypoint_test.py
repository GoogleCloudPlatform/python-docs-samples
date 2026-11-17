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

import pathlib
import runpy
from unittest import mock

from google.cloud import scheduler_v1
import pytest

SAMPLE = str(pathlib.Path(__file__).parent.parent / "get_job.py")
CLIENT = "google.cloud.scheduler_v1.CloudSchedulerClient"


def run_entrypoint(monkeypatch: pytest.MonkeyPatch, *flags: str) -> str:
    """Runs get_job.py as a script and returns the job name it requested."""
    monkeypatch.setattr("sys.argv", ["get_job.py", *flags])
    with mock.patch(CLIENT) as mock_client_class:
        client = mock_client_class.return_value
        client.get_job.return_value = scheduler_v1.Job(name="job")
        runpy.run_path(SAMPLE, run_name="__main__")
    return client.get_job.call_args.kwargs["request"].name


def test_entrypoint_reads_environment_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "env-project")
    monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", "europe-west1")
    monkeypatch.setenv("SCHEDULER_JOB_ID", "env-job")

    name = run_entrypoint(monkeypatch)

    assert name == "projects/env-project/locations/europe-west1/jobs/env-job"


def test_entrypoint_flags_override_environment_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "env-project")
    monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", "europe-west1")
    monkeypatch.setenv("SCHEDULER_JOB_ID", "env-job")

    name = run_entrypoint(monkeypatch, "--job-id", "flag-job")

    assert name == "projects/env-project/locations/europe-west1/jobs/flag-job"


def test_entrypoint_uses_example_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    for env_var in (
        "GOOGLE_CLOUD_PROJECT",
        "GOOGLE_CLOUD_LOCATION",
        "SCHEDULER_JOB_ID",
    ):
        monkeypatch.delenv(env_var, raising=False)

    name = run_entrypoint(monkeypatch)

    assert name == (
        "projects/example-project-id/locations/us-central1/jobs/example-job-id"
    )
