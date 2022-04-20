import importlib
import logging
import os
import platform
import sys
from typing import Dict
import uuid
from unittest.mock import patch, Mock

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
KERNEL_SIZE = 1
TRAINING_PATCH_SIZE = 1
PREDICTION_PATCH_SIZE = 2

DATAFLOW_CREATE_DATASETS_JOB_NAME = f"{NAME.replace('/', '-')}-{UUID}"

# Colab libraries are not available, so we disable them explicitly.
sys.modules["google.colab"] = Mock()


# Converting a notebook to Python source leaves us with the IPython magics
# as undefined methods, so we'll use a custom implementation for testing.
class PatchedIPython:
    @staticmethod
    def system(cmd):
        print(f"!{cmd}")


def get_ipython():
    return PatchedIPython()


# TODO: use these for export_points.csv
# [-123.26143117162316, 39.130692612214816, -117.63643117162316, 37.05582768877082]


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
        kernel_size=KERNEL_SIZE,
        training_patch_size=TRAINING_PATCH_SIZE,
        prediction_patch_size=PREDICTION_PATCH_SIZE,
    )


def test_land_cover_create_datasets_dataflow(run_notebook: None) -> None:
    # TODO:
    # - fixture: job_id from job name (wait until finish successfully)
    # - check that files exist
    pass


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
    kernel_size: int,
    training_patch_size: int,
    prediction_patch_size: int,
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
        "KERNEL_SIZE": str(kernel_size),
        "TRAINING_PATCH_SIZE": str(training_patch_size),
        "PREDICTION_PATCH_SIZE": str(prediction_patch_size),
        "DATAFLOW_CREATE_DATASETS_JOB_NAME": DATAFLOW_CREATE_DATASETS_JOB_NAME,
    }
    print("+" + "-" * 60)
    print(f"|  Environment variables")
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
    parser.add_argument("--kernel-size", default=KERNEL_SIZE, type=int)
    parser.add_argument("--training-patch-size", default=TRAINING_PATCH_SIZE, type=int)
    parser.add_argument(
        "--prediction-patch-size", default=PREDICTION_PATCH_SIZE, type=int
    )
    args = parser.parse_args()

    # For local testing, make sure you've run `ee.Authenticate()`.
    ee.Initialize()

    # Run the notebook.
    run(**vars(args))
