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

from google.cloud.workflows import executions_v1
import pytest

SAMPLE = str(
    pathlib.Path(__file__).resolve().parent.parent
    / "src"
    / "workflows_samples"
    / "execute_without_arguments.py"
)
CLIENT = "google.cloud.workflows.executions_v1.ExecutionsClient"
ENV_VARS = ("GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_LOCATION", "WORKFLOW_ID")


def run_entrypoint(monkeypatch: pytest.MonkeyPatch, *flags: str) -> str:
    """Runs execute_without_arguments.py as a script and returns its parent."""
    monkeypatch.setattr("sys.argv", ["execute_without_arguments.py", *flags])
    with mock.patch(CLIENT) as mock_client_class:
        client = mock_client_class.return_value
        done = executions_v1.Execution(
            name="execution", state=executions_v1.Execution.State.SUCCEEDED
        )
        client.create_execution.return_value = done
        client.get_execution.return_value = done
        runpy.run_path(SAMPLE, run_name="__main__")
    return client.create_execution.call_args.kwargs["parent"]


def test_entrypoint_reads_environment_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for env_var, value in zip(ENV_VARS, ("env-project", "europe-west1", "env-wf")):
        monkeypatch.setenv(env_var, value)

    parent = run_entrypoint(monkeypatch)

    assert parent == "projects/env-project/locations/europe-west1/workflows/env-wf"


def test_entrypoint_flags_override_environment_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for env_var, value in zip(ENV_VARS, ("env-project", "europe-west1", "env-wf")):
        monkeypatch.setenv(env_var, value)

    parent = run_entrypoint(monkeypatch, "--workflow-id", "flag-wf")

    assert parent == "projects/env-project/locations/europe-west1/workflows/flag-wf"


def test_entrypoint_uses_example_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    for env_var in ENV_VARS:
        monkeypatch.delenv(env_var, raising=False)

    parent = run_entrypoint(monkeypatch)

    assert parent == (
        "projects/example-project-id/locations/us-central1/workflows/myFirstWorkflow"
    )
