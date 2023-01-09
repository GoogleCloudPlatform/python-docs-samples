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

from datetime import datetime
import textwrap

# The conftest contains a bunch of reusable fixtures used all over the place.
# If we use a fixture not defined here, it must be on the conftest!
#   https://docs.pytest.org/en/latest/explanation/fixtures.html
import conftest  # python-docs-samples/people-and-planet-ai/conftest.py

import pytest

from weather.data import get_inputs_patch
from weather.model import WeatherModel

MODEL_PATH = "serving/model"


# ---------- FIXTURES ---------- #


@pytest.fixture(scope="session")
def test_name(python_version: str) -> str:
    # Many fixtures expect a fixture called `test_name`, so be sure to define it!
    return f"ppai/weather-py{python_version}"


@pytest.fixture(scope="session")
def install_local_packages() -> None:
    packages = ["serving/weather-data", "serving/weather-model"]
    conftest.run_cmd(["pip", "install"] + packages)


@pytest.fixture(scope="session")
def data_path_local(install_local_packages: None) -> str:
    path = "data"
    conftest.run_cmd(
        "python",
        "create_dataset.py",
        f"--data-path={path}",
        "--num-dates=1",
        "--num-bins=2",
    )
    return path


@pytest.fixture(scope="session")
def data_path_gcs(bucket_name: str, data_path_local: str) -> str:
    gcs_path = f"gs://{bucket_name}/weather/data/"
    conftest.run_cmd("gsutil", "-m", "cp", f"{data_path_local}/*.npz", gcs_path)
    return gcs_path


# ---------- TESTS ---------- #


def test_pretrained_model() -> None:
    patch_size = 16
    date = datetime(2019, 9, 3, 18)
    inputs = get_inputs_patch(date, (-90.0, 25.0), patch_size)

    model = WeatherModel.from_pretrained(MODEL_PATH)
    assert inputs.shape == (patch_size, patch_size, 52)
    predictions = model.predict(inputs.tolist())
    assert predictions.shape == (patch_size, patch_size, 2)


def test_weather_forecasting_notebook(
    unique_name: str,
    project: str,
    bucket_name: str,
    location: str,
    data_path_local: str,
    data_path_gcs: str,
) -> None:

    dataflow_dataset_flags = " ".join(
        [
            '--runner="DataflowRunner"',
            f"--job_name={unique_name}-dataset",
            "--num-dates=1",
            "--num-bins=2",
            "--max-requests=2",
        ]
    )

    conftest.run_notebook_parallel(
        "README.ipynb",
        prelude=textwrap.dedent(
            f"""\
            # Google Cloud resources.
            project = {repr(project)}
            bucket = {repr(bucket_name)}
            location = {repr(location)}
            """
        ),
        sections={
            "# 📚 Understand the data": {},
            "# 🗄 Create the dataset": {},
            "# ☁️ Create the dataset in Dataflow": {
                "replace": {'--runner="DataflowRunner"': dataflow_dataset_flags},
            },
            "# 🧠 Train the model": {"variables": {"data_path": data_path_local}},
            "# ☁️ Train the model in Vertex AI": {
                "variables": {"data_path": data_path_gcs, "epochs": 2}
            },
        },
    )
