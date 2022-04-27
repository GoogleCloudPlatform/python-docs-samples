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
import pytest


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


# Converting a notebook to Python source leaves us with the IPython magics
# as undefined methods, so we'll use a custom implementation for testing.
class PatchedIPython:
    @staticmethod
    def system(cmd: str) -> None:
        print(f"!{cmd}")


def get_ipython() -> PatchedIPython:
    return PatchedIPython()


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
def run_notebook(bucket_name: str) -> None:
    # Authenticate Earth Engine using the default credentials.
    credentials, _ = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/earthengine",
        ]
    )
    ee.Initialize(credentials, project=PROJECT)

    # Run the notebook.
    run(
        ipynb_file=IPYNB_FILE,
        py_file=PY_FILE,
        project=PROJECT,
        bucket=bucket_name,
        location=LOCATION,
    )


def test_land_cover_create_datasets_dataflow(bucket_name: str) -> None:
    training_file = f"gs://{bucket_name}/land-cover/training-data"
    validation_file = f"gs://{bucket_name}/land-cover/validation-data"
    points_per_region = 100
    training_patch_size = 8
    cmd = [
        "python",
        "create_datasets.py",
        f"--training-file={training_file}",
        f"--validation-file={validation_file}",
        "--regions-file=data/training-regions.csv",
        f"--points-per-region={points_per_region}",
        f"--patch-size={training_patch_size}",
        "--runner=DataflowRunner",
        f"--project={PROJECT}",
        f"--region={LOCATION}",
        f"--job_name={NAME.replace('/', '-')}-{UUID}",
        f"--temp_location=gs://{bucket_name}/land-cover/temp",
        "--setup_file=./setup.py",
    ]
    subprocess.check_call(cmd)

    # TODO: check the names and shapes on the training and validation files


# TODO: Not implemented
# def test_land_cover_predict_cloud_run(run_notebook: None) -> None:
#     # TODO:
#     # - fixture: service_url wait until it's deployed (with cleanup)
#     # - send a prediction
#     # - check shapes
#     pass


# TODO: Not implemented
# def test_land_cover_predict_dataflow(run_notebook: None) -> None:
#     # TODO:
#     # - fixture: job_id from job name (wait until finish successfully)
#     # -
#     pass


@patch("apache_beam.Pipeline", lambda **kwargs: TestPipeline())
def run(
    ipynb_file: str,
    py_file: str,
    project: str,
    bucket: str,
    location: str,
) -> None:
    # Convert the notebook file into a Python source file.
    with open(ipynb_file) as f:
        notebook = nbformat.read(f, as_version=4)
        nb_source, _ = nbconvert.PythonExporter().from_notebook_node(notebook)
        py_source = f"from test_utils import get_ipython\n{nb_source}"

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
    parser.add_argument("--ipynb-file", default=IPYNB_FILE)
    parser.add_argument("--py-file", default=PY_FILE)
    parser.add_argument("--location", default=LOCATION)
    args = parser.parse_args()

    # For local testing, make sure you've run `ee.Authenticate()`.
    ee.Initialize()

    # Run the notebook.
    run(**vars(args))
