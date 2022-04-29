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

import csv
import importlib
import logging
import os
import platform
import subprocess
import sys
from unittest.mock import Mock, patch
import uuid

from apache_beam.testing.test_pipeline import TestPipeline
import ee
import google.auth
from google.cloud import storage
import nbconvert
import nbformat
import numpy as np
import pytest

import batch_predict
import trainer

"""
For local testing, run `ee.Authenticate()` as a one-time step.

    export GOOGLE_CLOUD_PROJECT="my-project-id"
    export BUCKET="my-cloud-storage-bucket"
    python -c "import ee; ee.Authenticate()"
    python e2e_test.py --bucket $BUCKET
"""

PYTHON_VERSION = "".join(platform.python_version_tuple()[0:2])

NAME = f"ppai/land-cover-py{PYTHON_VERSION}"

UUID = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = "us-central1"

IPYNB_FILE = "README.ipynb"
PY_FILE = "README.py"

# Colab libraries are not available, so we disable them explicitly.
sys.modules["google.colab"] = Mock()


# Add more logging information for debugging.
logging.getLogger().setLevel(logging.INFO)


@pytest.fixture(scope="session")
def bucket_name() -> str:
    storage_client = storage.Client()

    bucket_name = f"{NAME.replace('/', '-')}-{UUID}"
    bucket = storage_client.create_bucket(bucket_name, location=LOCATION)

    logging.info(f"bucket_name: {bucket_name}")
    yield bucket_name

    bucket.delete(force=True)


@pytest.fixture(scope="session")
def container_image() -> str:
    # https://cloud.google.com/sdk/gcloud/reference/builds/submit
    container_image = f"gcr.io/{PROJECT}/{NAME}:{UUID}"
    # gcloud builds submit --pack image=gcr.io/{project}/land-cover:latest serving/
    subprocess.check_call(
        [
            "gcloud",
            "builds",
            "submit",
            f"--project={PROJECT}",
            "--pack",
            f"image={container_image}",
            "serving/",
            "--machine-type=e2-highcpu-8",
            "--quiet",
        ]
    )

    logging.info(f"container_image: {container_image}")
    yield container_image

    # https://cloud.google.com/sdk/gcloud/reference/container/images/delete
    subprocess.check_call(
        [
            "gcloud",
            "container",
            "images",
            "delete",
            container_image,
            f"--project={PROJECT}",
            "--force-delete-tags",
            "--quiet",
        ]
    )


@pytest.fixture(scope="session")
def service_url(container_image: str) -> str:
    # https://cloud.google.com/sdk/gcloud/reference/run/deploy
    service_name = f"{NAME.replace('/', '-')}-{UUID}"
    subprocess.check_call(
        [
            "gcloud",
            "run",
            "deploy",
            service_name,
            f"--project={PROJECT}",
            f"--image={container_image}",
            f"--region={LOCATION}",
            "--no-allow-unauthenticated",
        ]
    )

    # https://cloud.google.com/sdk/gcloud/reference/run/services/describe
    service_url = (
        subprocess.run(
            [
                "gcloud",
                "run",
                "services",
                "describe",
                service_name,
                f"--project={PROJECT}",
                f"--region={LOCATION}",
                "--format=get(status.url)",
            ],
            capture_output=True,
        )
        .stdout.decode("utf-8")
        .strip()
    )

    logging.info(f"service_url: {service_url}")
    yield service_url

    # https://cloud.google.com/sdk/gcloud/reference/run/services/delete
    subprocess.check_call(
        [
            "gcloud",
            "run",
            "services",
            "delete",
            service_name,
            "--platform=managed",
            f"--project={PROJECT}",
            f"--region={LOCATION}",
            "--quiet",
        ]
    )


@pytest.fixture(scope="session")
def identity_token() -> str:
    yield (
        subprocess.run(
            ["gcloud", "auth", "print-identity-token", f"--project={PROJECT}"],
            capture_output=True,
        )
        .stdout.decode("utf-8")
        .strip()
    )


def test_notebook(bucket_name: str) -> None:
    # Authenticate Earth Engine using the default credentials.
    credentials, _ = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/earthengine",
        ]
    )
    ee.Initialize(credentials, project=PROJECT)

    # First, create prediction files with the right shapes to test displaying results.
    with open("data/prediction-locations.csv") as f:
        predictions_prefix = f"gs://{bucket_name}/land-cover/predictions"
        inputs = np.array(
            [np.zeros(shape=(16, 16)) for _ in trainer.INPUT_BANDS],
            dtype=[(name, "<f8") for name in trainer.INPUT_BANDS],
        )
        outputs = np.zeros(shape=(16, 16, 9))
        for name in {row["name"] for row in csv.DictReader(f)}:
            results = {"name": name, "inputs": inputs, "outputs": outputs}
            batch_predict.write_to_numpy(results, predictions_prefix)

    # Run the notebook.
    run(
        project=PROJECT,
        bucket=bucket_name,
        location=LOCATION,
        ipynb_file=IPYNB_FILE,
        py_file=PY_FILE,
    )


def test_land_cover_create_datasets_dataflow(bucket_name: str) -> None:
    training_prefix = f"gs://{bucket_name}/land-cover/training-data"
    validation_prefix = f"gs://{bucket_name}/land-cover/validation-data"
    points_per_region = 100
    patch_size = 16
    batch_size = 32

    # ℹ️ If this command changes, please update the corresponding command at the
    #   "🚄 Create the datasets in Dataflow" section in the `README.ipynb` notebook.
    cmd = [
        "python",
        "create_datasets.py",
        f"--training-prefix={training_prefix}",
        f"--validation-prefix={validation_prefix}",
        f"--points-per-region={points_per_region}",
        f"--patch-size={patch_size}",
        "--runner=DataflowRunner",
        f"--project={PROJECT}",
        f"--region={LOCATION}",
        f"--job_name={NAME.replace('/', '-')}-training-{UUID}",  # not used in notebook
        f"--temp_location=gs://{bucket_name}/land-cover/temp",
        "--setup_file=./setup.py",
    ]
    subprocess.check_call(cmd)

    def validate_dataset(data_path_prefix: str) -> None:
        data_path = f"{data_path_prefix}*.tfrecord.gz"
        dataset = trainer.read_dataset(data_path, patch_size, batch_size)
        x, y = [pair for pair in dataset.take(1)][0]

        expected_shape = (batch_size, patch_size, patch_size, 13)
        assert (
            x.shape == expected_shape
        ), f"expected shape {expected_shape}, but got {x.shape} for inputs in {data_path}"

        expected_shape = (batch_size, patch_size, patch_size, 9)
        assert (
            y.shape == expected_shape
        ), f"expected shape {expected_shape}, but got {y.shape} for outputs in {data_path}"

    # Make sure the training dataset is valid.
    validate_dataset(training_prefix)
    validate_dataset(validation_prefix)


def test_land_cover_train_model_vertex_ai(service_url: str) -> None:
    # ℹ️ If this command changes, please update the corresponding command at the
    #   "🧠 Train the model in Vertex AI" section in the `README.ipynb` notebook.
    # TODO:
    #   - check the model directory was created
    pass


def test_land_cover_predict_cloud_run(service_url: str) -> None:
    # ℹ️ If this command changes, please update the corresponding command at the
    #   "📞 Online predictions in Cloud Run" section in the `README.ipynb` notebook.
    # TODO:
    # - check input and output shapes
    pass


def test_land_cover_predict_dataflow() -> None:
    # ℹ️ If this command changes, please update the corresponding command at the
    #   "🧺 Batch predictions in Dataflow" section in the `README.ipynb` notebook.
    # TODO:
    # - check input and output shapes
    pass


@patch("apache_beam.Pipeline", lambda **kwargs: TestPipeline())
@patch("google.cloud.aiplatform.CustomTrainingJob.run", Mock())
def run(
    project: str,
    bucket: str,
    location: str,
    ipynb_file: str,
    py_file: str,
) -> None:
    # Convert the notebook file into a Python source file.
    with open(ipynb_file) as f:
        notebook = nbformat.read(f, as_version=4)
        py_source = "\n".join(
            [
                "from unittest.mock import Mock",
                "get_ipython = Mock()",
                nbconvert.PythonExporter().from_notebook_node(notebook)[0],
            ]
        )

    with open(py_file, "w") as f:
        f.write(py_source)

    # Set up the environment variables to inject into the notebook code.
    env = {
        "GOOGLE_CLOUD_PROJECT": project,
        "CLOUD_STORAGE_BUCKET": bucket,
        "CLOUD_LOCATION": location,
    }
    print("+" + "-" * 60)
    print("|  Environment variables")
    print("+" + "-" * 60)
    for name, value in env.items():
        print(f"{name} = {value}")
    print("+" + "-" * 60)

    try:
        # Importing the module runs the notebook code as a side effect.
        print(f">> Running {py_file} (auto-generated from {ipynb_file})")
        with patch.dict(os.environ, env), patch("ee.Initialize", Mock()):
            module_name = os.path.splitext(py_file)[0]
            importlib.import_module(module_name)

    except Exception as error:
        # Something failed, print the source code for debugging.
        print("+" + "-" * 60)
        print(f"|  {py_file} (auto-generated from {ipynb_file})")
        print("+" + "-" * 60)
        for i, line in enumerate(py_source.splitlines()):
            print(f"{i + 1 :4}| {line}")
        print("+" + "-" * 60)
        raise error


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--project", default=PROJECT)
    parser.add_argument("--location", default=LOCATION)
    parser.add_argument("--ipynb-file", default=IPYNB_FILE)
    parser.add_argument("--py-file", default=PY_FILE)
    args = parser.parse_args()

    # For local testing, make sure you've run `ee.Authenticate()`.
    ee.Initialize()

    # Run the notebook.
    run(**vars(args))
