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
import io
import logging
import os
import platform
import subprocess
import sys
from unittest.mock import Mock, patch
import uuid

import apache_beam as beam
from apache_beam.io.filesystems import FileSystems
from apache_beam.testing.test_pipeline import TestPipeline
import ee
import google.auth
from google.cloud import aiplatform
from google.cloud import storage
import nbconvert
import nbformat
import numpy as np
import pytest
import requests
import tensorflow as tf

import batch_predict
import create_datasets
import trainer


PYTHON_VERSION = "".join(platform.python_version_tuple()[0:2])

NAME = f"ppai/land-cover-py{PYTHON_VERSION}"

UUID = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = "us-central1"

IPYNB_FILE = "README.ipynb"
PY_FILE = "README.py"

PATCH_SIZE = 16
INPUTS_DTYPE = [(name, "<f8") for name in trainer.INPUT_BANDS]
NUM_CLASSES = trainer.NUM_CLASSIFICATIONS

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

    subprocess.check_call(["gsutil", "-m", "rm", "-rf", f"gs://{bucket_name}/*"])
    bucket.delete(force=True)


@pytest.fixture(scope="session")
def container_image() -> str:
    # https://cloud.google.com/sdk/gcloud/reference/builds/submit
    container_image = f"gcr.io/{PROJECT}/{NAME}:{UUID}"
    subprocess.check_call(
        [
            "gcloud",
            "builds",
            "submit",
            f"--project={PROJECT}",
            f"--tag={container_image}",
            "serving/",
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
def service_url(bucket_name: str, container_image: str) -> str:
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
            f"--update-env-vars=MODEL_PATH=gs://{bucket_name}/land-cover/model",
            "--memory=1G",
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


@pytest.fixture(scope="session")
def pretrained_model(bucket_name: str) -> None:
    model_path = f"gs://{bucket_name}/land-cover/model/"
    cmd = [
        "gsutil",
        "-m",
        "cp",
        "-R",
        "data/model/*",
        model_path,
    ]
    subprocess.check_call(cmd)
    yield model_path


def test_notebook(bucket_name: str) -> None:
    # Authenticate Earth Engine using the default credentials.
    credentials, _ = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/earthengine",
        ]
    )
    ee.Initialize(
        credentials,
        project=PROJECT,
        opt_url="https://earthengine-highvolume.googleapis.com",
    )

    # First, create prediction files with the right shapes to test displaying results.
    write_numpy_predictions("results")
    with open("data/prediction-locations.csv") as f:
        predictions_prefix = f"gs://{bucket_name}/land-cover/predictions"
        for row in csv.DictReader(f):
            write_numpy_predictions(f"{row['name']}/{row['year']}", predictions_prefix)

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
    points_per_region = 10
    batch_size = 32

    # ℹ️ If this command changes, please update the corresponding command at the
    #   "🚄 Create the datasets in Dataflow" section in the `README.ipynb` notebook.
    cmd = [
        "python",
        "create_datasets.py",
        f"--training-prefix={training_prefix}",
        f"--validation-prefix={validation_prefix}",
        f"--points-per-region={points_per_region}",
        f"--patch-size={PATCH_SIZE}",
        "--runner=DataflowRunner",
        f"--project={PROJECT}",
        f"--region={LOCATION}",
        f"--temp_location=gs://{bucket_name}/land-cover/temp",
        "--setup_file=./setup.py",
        # Parameters for testing only, not used in the notebook.
        f"--job_name={NAME.replace('/', '-')}-training-{UUID}",
        "--max_num_workers=10",
    ]
    subprocess.check_call(cmd)

    def validate_dataset(data_path_prefix: str) -> None:
        data_path = f"{data_path_prefix}*.tfrecord.gz"
        dataset = trainer.read_dataset(data_path, PATCH_SIZE, batch_size)
        inputs, outputs = [pair for pair in dataset.take(1)][0]
        assert set(inputs.keys()) == set(trainer.INPUT_BANDS)
        for values in inputs.values():
            assert values.shape == (batch_size, PATCH_SIZE, PATCH_SIZE)
        assert outputs.shape == (batch_size, PATCH_SIZE, PATCH_SIZE, NUM_CLASSES)

    # Make sure the training dataset is valid.
    validate_dataset(training_prefix)
    validate_dataset(validation_prefix)


def test_land_cover_train_model_vertex_ai(bucket_name: str) -> None:
    aiplatform.init(project=PROJECT, location=LOCATION, staging_bucket=bucket_name)

    write_tfrecords(f"gs://{bucket_name}/land-cover/datasets")

    # ℹ️ If these commands change, please update the corresponding commands at the
    #   "🧠 Train the model in Vertex AI" section in the `README.ipynb` notebook.
    job = aiplatform.CustomTrainingJob(
        display_name=f"{NAME.replace('/', '_').replace('-', '_')}_{UUID}",
        script_path="trainer.py",
        container_uri="us-docker.pkg.dev/vertex-ai/training/tf-gpu.2-8:latest",
    )
    job.run(
        accelerator_type="NVIDIA_TESLA_T4",
        accelerator_count=1,
        args=[
            f"--training-data=gs://{bucket_name}/land-cover/datasets/training/*.tfrecord.gz",
            f"--validation-data=gs://{bucket_name}/land-cover/datasets/validation/*.tfrecord.gz",
            f"--model-path=gs://{bucket_name}/land-cover/model-vertex",
            f"--patch-size={PATCH_SIZE}",
            "--epochs=10",
        ],
    )

    # Make sure the model works.
    model = tf.keras.models.load_model(f"gs://{bucket_name}/land-cover/model-vertex")
    with open("data/prediction-locations.csv") as f:
        region = next(csv.DictReader(f))
    _, patch = batch_predict.get_prediction_patch(
        region, trainer.INPUT_BANDS, PATCH_SIZE
    )
    inputs_batch = {name: np.stack([patch[name]]) for name in patch.dtype.names}
    probabilities = model.predict(inputs_batch)
    assert probabilities.shape == (1, PATCH_SIZE, PATCH_SIZE, NUM_CLASSES)


def test_land_cover_batch_predict_dataflow(
    bucket_name: str, pretrained_model: str
) -> None:
    # ℹ️ If this command changes, please update the corresponding command at the
    #   "🧺 Batch predictions in Dataflow" section in the `README.ipynb` notebook.
    cmd = [
        "python",
        "batch_predict.py",
        f"--model-path={pretrained_model}",
        f"--predictions-prefix=gs://{bucket_name}/land-cover/predictions",
        f"--patch-size={PATCH_SIZE}",
        "--runner=DataflowRunner",
        f"--project={PROJECT}",
        f"--region={LOCATION}",
        f"--temp_location=gs://{bucket_name}/land-cover/temp",
        "--setup_file=./setup.py",
        # Parameters for testing only, not used in the notebook.
        f"--job_name={NAME.replace('/', '-')}-prediction-{UUID}",
        "--max_num_workers=10",
    ]
    subprocess.check_call(cmd)

    with open("data/prediction-locations.csv") as f:
        for region in csv.DictReader(f):
            name = region["name"]
            year = region["year"]
            filename = f"gs://{bucket_name}/land-cover/predictions/{name}/{year}.npz"
            with FileSystems.open(filename) as f:
                npz_file = np.load(f)
                inputs, outputs = (npz_file["inputs"], npz_file["outputs"])
                assert inputs.shape == (PATCH_SIZE, PATCH_SIZE)
                assert inputs.dtype.names == tuple(trainer.INPUT_BANDS)
                assert outputs.shape == (PATCH_SIZE, PATCH_SIZE)


def test_land_cover_online_predict_cloud_run(
    pretrained_model: str, service_url: str, identity_token: str
) -> None:
    response = requests.get(
        f"{service_url}/predict/39.781/-121.526/2018",
        headers={"Authorization": f"Bearer {identity_token}"},
        params={"model-path": pretrained_model, "patch-size": PATCH_SIZE},
    )
    if response.status_code != 200:
        print(response.text)
    response.raise_for_status()

    npz_file = np.load(io.BytesIO(response.content))
    assert npz_file["inputs"].shape == (PATCH_SIZE, PATCH_SIZE)
    assert npz_file["inputs"].dtype.names == tuple(trainer.INPUT_BANDS)
    assert npz_file["outputs"].shape == (PATCH_SIZE, PATCH_SIZE)


@patch("apache_beam.Pipeline", lambda **kwargs: TestPipeline())
@patch("google.cloud.aiplatform.CustomTrainingJob.run", Mock())
def run(
    project: str,
    bucket: str,
    location: str,
    points_per_region: int = 1,
    ipynb_file: str = IPYNB_FILE,
    py_file: str = PY_FILE,
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
        "POINTS_PER_REGION": str(points_per_region),
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


def write_numpy_predictions(name: str, path_prefix: str = ".") -> str:
    results = {
        "filename": name,
        "inputs": np.zeros(
            shape=(PATCH_SIZE, PATCH_SIZE),
            dtype=[(name, np.float64) for name in trainer.INPUT_BANDS],
        ),
        "outputs": np.zeros(shape=(PATCH_SIZE, PATCH_SIZE), dtype=np.uint8),
    }
    filename = batch_predict.write_to_numpy(results, path_prefix)
    print(f"Created {filename}")
    return filename


def write_tfrecords(path_prefix: str) -> str:
    bands = trainer.INPUT_BANDS + trainer.OUTPUT_BANDS
    patch = np.zeros(
        shape=(PATCH_SIZE, PATCH_SIZE),
        dtype=[(name, np.float64) for name in bands],
    )
    serialized = create_datasets.serialize(patch)

    with beam.Pipeline() as pipeline:
        data = pipeline | beam.Create([serialized] * 10)
        data | "Write training" >> beam.io.WriteToTFRecord(
            f"{path_prefix}/training/data", file_name_suffix=".tfrecord.gz"
        )
        data | "Write validation" >> beam.io.WriteToTFRecord(
            f"{path_prefix}/validation/data", file_name_suffix=".tfrecord.gz"
        )
