import logging
import os
import platform
import sys
import uuid

import ee
import google.auth
from google.cloud import storage
import nbconvert
import nbformat
import pytest

from unittest import mock

PYTHON_VERSION = "".join(platform.python_version_tuple()[0:2])

NAME = f"ppai/geospatial-classification-py{PYTHON_VERSION}"

UUID = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = "us-central1"

# TODO: use these for export_points.csv
# [-123.26143117162316, 39.130692612214816, -117.63643117162316, 37.05582768877082]


try:
    # For Colab and service accounts we use the default credentials.
    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    ee.Initialize(credentials, project=PROJECT)
except:
    # When running locally EE doesn't like the default credentials.
    # ee.Authenticate()
    ee.Initialize()


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
@mock.patch("ee.Initialize", mock.Mock())
@mock.patch("ee.batch.Export.table.toCloudStorage", mock.Mock())  # TODO: REMOVE THIS
def run_notebook() -> None:
    sys.modules["google.colab"] = mock.Mock()
    get_ipython = mock.Mock()

    # Convert the notebook into a Python script and run it.
    with open("TEST.ipynb") as f:
        notebook = nbformat.read(f, as_version=4)
        exporter = nbconvert.PythonExporter()
        py_source, _ = exporter.from_notebook_node(notebook)

        # Print the Python source for debugging.
        print("+" + "-" * 60)
        print("|  README.py (generated from README.ipynb)")
        print("+" + "-" * 60)
        for i, line in enumerate(py_source.splitlines()):
            print(f"{i + 1 :4}| {line}")
        print("+" + "-" * 60)

        # Set up for the testing infrastructure.
        os.environ["CLOUD_STORAGE_BUCKET"] = "dcavazos-lyra"
        os.environ["CLOUD_LOCATION"] = "us-central1"
        os.environ["POINTS_PER_CLASS"] = "1"
        os.environ["PADDING"] = "1"

        # Compile and run the notebook code.
        exec(compile(py_source, "README.py", "exec"))


def test_land_cover_export_data(run_notebook: None) -> None:
    assert False
