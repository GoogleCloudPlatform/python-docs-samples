#!/usr/bin/env python

# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""End-to-end tests.

To use an existing bucket, set it without the 'gs://' prefix:
    GOOGLE_CLOUD_BUCKET="my-bucket-name"

Run with `pytest` (local environment):
    # Run all tests.
    PYTHONPATH=.. pytest -s tests/e2e_test.py

    # Run a single test.
    PYTHONPATH=.. pytest -s tests/e2e_test.py -k test_name

Run with `nox` (clean virtual environment):
    nox -s lint
    nox -s py-3.11
"""

from __future__ import annotations

import tempfile

import conftest  # python-docs-samples/dataflow/conftest.py

import pytest

MODEL_NAME = "google/flan-t5-small"


@pytest.fixture(scope="session")
def test_name() -> str:
    # Many fixtures expect a fixture called `test_name`, so be sure to define it!
    return "dataflow/run-inference"


@pytest.fixture(scope="session")
def state_dict_path(bucket_name: str) -> str:
    gcs_path = f"gs://{bucket_name}/temp/state_dict.pt"
    with tempfile.NamedTemporaryFile("w") as f:
        # To avoid test timeouts, load the state dict locally.
        # It's small enough to safely fit into memory and disk.
        conftest.run_cmd(
            "python",
            "load-state-dict.py",
            "local",
            f"--model-name={MODEL_NAME}",
            f"--state-dict-path={f.name}",
        )

        # Then copy it to Cloud Storage.
        conftest.run_cmd("gsutil", "cp", "-n", f.name, gcs_path)
    return gcs_path


def test_load_state_dict_vertex(
    project: str,
    bucket_name: str,
    location: str,
    unique_name: str,
) -> None:
    conftest.run_cmd(
        "python",
        "load-state-dict.py",
        "vertex",
        f"--model-name={MODEL_NAME}",
        f"--state-dict-path=gs://{bucket_name}/temp/state_dict_vertex.pt",
        f"--job-name={unique_name}",
        f"--project={project}",
        f"--bucket={bucket_name}",
        f"--location={location}",
    )


def test_pipeline_local(state_dict_path: str) -> None:
    conftest.run_cmd(
        "python",
        "main.py",
        f"--input-topic=unused",
        f"--output-topic=unused",
        f"--model-name={MODEL_NAME}",
        f"--state-dict-path={state_dict_path}",
    )


def test_pipeline_dataflow(
    project: str,
    bucket_name: str,
    location: str,
    unique_name: str,
    state_dict_path: str,
) -> None:
    conftest.run_cmd(
        "python",
        "main.py",
        f"--model-name={MODEL_NAME}",
        f"--state-dict-path={state_dict_path}",
        "--runner=DataflowRunner",
        f"--job_name={unique_name}",
        f"--project={project}",
        f"--temp_location=gs://{bucket_name}/temp",
        f"--region={location}",
    )
