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
import os
import tempfile
import textwrap

# The conftest contains a bunch of reusable fixtures used all over the place.
# If we use a fixture not defined here, it must be on the conftest!
#   https://docs.pytest.org/en/latest/explanation/fixtures.html
import conftest  # python-docs-samples/people-and-planet-ai/conftest.py

import numpy as np
import pytest

from weather.data import get_inputs_patch, get_labels_patch

os.chdir(os.path.join("..", ".."))


@pytest.fixture(scope="session")
def test_name() -> str:
    # Many fixtures expect a fixture called `test_name`, so be sure to define it!
    return "ppai/weather-dataset"


@pytest.fixture(scope="session")
def data_path_gcs(bucket_name: str) -> str:
    path_gcs = f"gs://{bucket_name}/test/weather/data-training"
    date = datetime(2019, 9, 2, 18)
    point = (-69.55, -39.82)
    patch_size = 8
    inputs = get_inputs_patch(date, point, patch_size)
    labels = get_labels_patch(date, point, patch_size)
    with tempfile.NamedTemporaryFile() as f:
        batch_size = 16
        inputs_batch = [inputs] * batch_size
        labels_batch = [labels] * batch_size
        np.savez_compressed(f, inputs=inputs_batch, labels=labels_batch)
        conftest.run_cmd("gsutil", "cp", f.name, f"{path_gcs}/example.npz")
    return path_gcs


def test_train_model(
    project: str,
    bucket_name: str,
    location: str,
    data_path_gcs: str,
    unique_name: str,
) -> None:
    conftest.run_notebook_parallel(
        os.path.join("notebooks", "3-training.ipynb"),
        prelude=textwrap.dedent(
            f"""\
            # Google Cloud resources.
            project = {repr(project)}
            bucket = {repr(bucket_name)}
            location = {repr(location)}
            """
        ),
        sections={
            "# 🧠 Train the model locally": {
                "variables": {"data_path_gcs": data_path_gcs, "epochs": 2}
            },
            "# ☁️ Train the model in Vertex AI": {
                "variables": {
                    "display_name": unique_name,
                    "data_path": data_path_gcs.replace("gs://", "/gcs/"),
                    "model_path": f"/gcs/{bucket_name}/test/weather/model-vertex",
                    "epochs": 2,
                }
            },
        },
    )
