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

from __future__ import annotations

from collections.abc import Iterator
import os
import textwrap

# The conftest contains a bunch of reusable fixtures used all over the place.
# If we use a fixture not defined here, it must be on the conftest!
#   https://docs.pytest.org/en/latest/explanation/fixtures.html
import conftest  # python-docs-samples/people-and-planet-ai/conftest.py

import pytest

os.chdir(os.path.join("..", ".."))


@pytest.fixture(scope="session")
def test_name() -> str:
    # Many fixtures expect a fixture called `test_name`, so be sure to define it!
    return "ppai/weather-predictions"


@pytest.fixture(scope="session")
def model_path_gcs(bucket_name: str) -> str:
    path_gcs = f"gs://{bucket_name}/model"
    conftest.run_cmd("gsutil", "cp", "serving/model/*", path_gcs)
    return path_gcs


@pytest.fixture(scope="session")
def service_name(unique_name: str, location: str) -> Iterator[str]:
    # The service itself is created in the notebook.
    yield unique_name
    conftest.cloud_run_cleanup(unique_name, location)


def test_predictions(
    project: str,
    bucket_name: str,
    location: str,
    identity_token: str,
    service_name: str,
    model_path_gcs: str,
) -> None:
    conftest.run_notebook_parallel(
        os.path.join("notebooks", "4-predictions.ipynb"),
        prelude=textwrap.dedent(
            f"""\
            # Google Cloud resources.
            project = {repr(project)}
            bucket = {repr(bucket_name)}
            location = {repr(location)}
            """
        ),
        sections={
            "# 💻 Local predictions": {"variables": {"model_path_gcs": model_path_gcs}},
            "# ☁️ Cloud Run predictions": {
                "variables": {
                    "service_name": service_name,
                    "identity_token": identity_token,
                }
            },
        },
    )
