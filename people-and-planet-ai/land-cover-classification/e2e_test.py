import logging
import os
import platform
import sys
import uuid
from unittest.mock import patch, Mock

from apache_beam.testing.test_pipeline import TestPipeline
import ee
import google.auth
from google.cloud import storage
import nbconvert
import nbformat
import pytest


# For local testing, run `ee.Authenticate()` as a one-time step.
#
#   export GOOGLE_CLOUD_PROJECT="my-project-id"
#   python -c "import ee; ee.Authenticate()"
#   pytest -v e2e_test.py

PYTHON_VERSION = "".join(platform.python_version_tuple()[0:2])

NAME = f"ppai/land-cover-py{PYTHON_VERSION}"

UUID = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = "us-central1"

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
    # storage_client = storage.Client()

    # bucket_name = f"{NAME.replace('/', '-')}-{UUID}"
    # bucket = storage_client.create_bucket(bucket_name, location=LOCATION)

    bucket_name = "dcavazos-lyra"  # TODO: REMOVE THIS
    logging.info(f"bucket_name: {bucket_name}")
    yield bucket_name

    # bucket.delete(force=True)


@pytest.fixture(scope="session")
@patch("apache_beam.Pipeline", lambda **kwargs: TestPipeline())
def run_notebook(bucket_name: str) -> None:
    # Convert the notebook into a Python script and run it.
    with open("README.ipynb") as f:
        notebook = nbformat.read(f, as_version=4)
        nb_source, _ = nbconvert.PythonExporter().from_notebook_node(notebook)
        py_source = f"from test_utils import get_ipython\n{nb_source}"

    with open("README.py", "w") as f:
        f.write(py_source)

    # Manually authenticate before running the notebook code since
    # we're explicitly disabling the Colab authentication.
    try:
        # This works for the testing infrastructure and service accounts.
        credentials, _ = google.auth.default(
            scopes=[
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/earthengine",
            ]
        )
        ee.Initialize(credentials, project=PROJECT)
    except:
        # For local testing, make sure you've run `ee.Authenticate()`.
        ee.Initialize()

    # Set up the environment variables to inject into the notebook code.
    env = {
        "CLOUD_STORAGE_BUCKET": bucket_name,
        "CLOUD_LOCATION": LOCATION,
        "KERNEL_SIZE": "1",
        "TRAINING_PATCH_SIZE": "1",
        "PREDICTION_PATCH_SIZE": "2",
    }

    try:
        # Importing the module runs the notebook code as a side effect.
        with patch.dict(os.environ, env), patch("ee.Initialize", Mock()):
            import README

    except Exception as error:
        # Something failed, print the source code for debugging.
        print("+" + "-" * 60)
        print("|  README.py (auto-generated from README.ipynb)")
        print("+" + "-" * 60)
        for i, line in enumerate(py_source.splitlines()):
            print(f"{i + 1 :4}| {line}")
        print("+" + "-" * 60)
        raise error


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
