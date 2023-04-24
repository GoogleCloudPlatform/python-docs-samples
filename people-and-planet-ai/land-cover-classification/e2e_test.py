# Copyright 2022 Google LLC
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

from collections.abc import Iterable
import tempfile
import textwrap

# The conftest contains a bunch of reusable fixtures used all over the place.
# If we use a fixture not defined here, it must be on the conftest!
#   https://docs.pytest.org/en/latest/explanation/fixtures.html
import conftest  # python-docs-samples/people-and-planet-ai/conftest.py
import pytest
import tensorflow as tf

from serving import data
from trainer.tf_model import NUM_CLASSES, NUM_INPUTS


# ---------- FIXTURES ---------- #


@pytest.fixture(scope="session")
def test_name(python_version: str) -> str:
    # Many fixtures expect a fixture called `test_name`, so be sure to define it!
    return f"ppai/land-cover-py{python_version}"


@pytest.fixture(scope="session")
def data_path(bucket_name: str) -> str:
    # The Vertex AI training expects data here.
    gcs_path = f"gs://{bucket_name}/land-cover/data"
    conftest.run_cmd(
        "python",
        "create_dataset.py",
        "tensorflow",
        f"--data-path={gcs_path}",
        "--points-per-class=1",
        "--max-requests=1",
    )
    return gcs_path


@pytest.fixture(scope="session")
def model_path(bucket_name: str) -> str:
    # This is a different path than where Vertex AI saves its model.
    gcs_path = f"gs://{bucket_name}/pretrained-model"
    conftest.run_cmd("gsutil", "-m", "cp", "-r", "./pretrained-model", gcs_path)
    return gcs_path


@pytest.fixture(scope="session")
def cloud_run_service_name(unique_name: str, location: str) -> Iterable[str]:
    # The notebook itself creates the service.
    service_name = unique_name
    yield service_name
    conftest.cloud_run_cleanup(service_name, location)


@pytest.fixture(scope="session")
def aiplatform_model_name(unique_name: str, location: str) -> Iterable[str]:
    # The notebook itself creates the service.
    model_name = unique_name.replace("-", "_")
    yield model_name
    # Version "v1" is hardcoded in the notebook.
    conftest.aiplatform_cleanup(model_name, location, versions=["v1"])


# ---------- TESTS ---------- #


def test_pretrained_model() -> None:
    data.ee_init()
    patch_size = 64
    inputs = data.get_input_patch(2018, (-121.526, 39.781), patch_size)
    tf.ensure_shape(inputs, [patch_size, patch_size, NUM_INPUTS])
    model = tf.keras.models.load_model("pretrained-model")
    probabilities = model.predict(tf.stack([inputs]))[0]
    tf.ensure_shape(probabilities, [patch_size, patch_size, NUM_CLASSES])


def test_readme(project: str) -> None:
    conftest.run_notebook(
        "README.ipynb",
        prelude=textwrap.dedent(
            f"""\
            from serving.data import ee_init

            # Google Cloud resources.
            project = {repr(project)}

            # Initialize Earth Engine.
            ee_init()
            """
        ),
        section="# 📚 Understand the data",
        until_end=True,
    )


def test_land_cover_change(project: str) -> None:
    conftest.run_notebook(
        "land-cover-change.ipynb",
        prelude=textwrap.dedent(
            f"""\
            from serving.data import ee_init

            # Google Cloud resources.
            project = {repr(project)}

            # Initialize Earth Engine.
            ee_init()
            """
        ),
        section="# 🗾 Visualize changes in the land",
        until_end=True,
    )


def test_land_cover_tensorflow(
    project: str,
    bucket_name: str,
    location: str,
    unique_name: str,
    data_path: str,
    model_path: str,
    cloud_run_service_name: str,
    aiplatform_model_name: str,
    identity_token: str,
) -> None:
    # For Dataflow batch prediction, only grab the first location to shorten the runtime.
    with open("predict-locations.csv") as f:
        # Grab the header row and first entry.
        subset = f.readlines()[:2]

    with tempfile.NamedTemporaryFile("w") as locations_file:
        for line in subset:
            locations_file.write(line)
        locations_file.flush()

        conftest.run_notebook_parallel(
            "cloud-tensorflow.ipynb",
            prelude=textwrap.dedent(
                f"""\
                from serving.data import ee_init

                # Google Cloud resources.
                project = {repr(project)}
                bucket = {repr(bucket_name)}
                location = {repr(location)}

                # Initialize Earth Engine.
                ee_init()
                """
            ),
            sections={
                "# 📚 Understand the data": {},
                "# 🗄 Create the dataset": {
                    "variables": {
                        "points_per_class": 1,
                        "--data-path": f"gs://{bucket_name}/dataflow-data",
                    },
                    "replace": {
                        '--runner="DataflowRunner"': " ".join(
                            [
                                '--runner="DataflowRunner"',
                                f"--job_name={unique_name}-dataset",
                                "--max-requests=1",
                            ]
                        )
                    },
                },
                "# 🧠 Train the model": {
                    "variables": {
                        "display_name": unique_name,
                        "data_path": data_path,
                        "epochs": 1,
                    },
                },
                "## 💻 Local predictions": {
                    "variables": {
                        "model_path": model_path,
                    },
                },
                "## ☁️ Cloud Run predictions": {
                    "variables": {
                        "service_name": cloud_run_service_name,
                        "model_path": model_path,
                        "identity_token": identity_token,
                    },
                },
                "## 🧺 Dataflow batch prediction": {
                    "variables": {
                        "model_path": model_path,
                    },
                    "replace": {
                        '--runner="DataflowRunner"': " ".join(
                            [
                                '--runner="DataflowRunner"',
                                f"--job_name={unique_name}-predict",
                                "--max-requests=1",
                                f"--locations-file={locations_file.name}",
                            ]
                        )
                    },
                },
                "## 🌍 Earth Engine with AI Platform": {
                    "variables": {
                        "model_name": aiplatform_model_name,
                        "model_path": model_path,
                    },
                },
            },
        )
