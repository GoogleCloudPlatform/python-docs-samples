# Copyright 2021 Google LLC
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

import logging
import os
import platform
import subprocess
import time
import uuid
import json
import pandas as pd
import numpy as np

from google.cloud import aiplatform
from google.cloud import storage
import pytest
import requests

import ee
import google.auth

credentials, project = google.auth.default()
ee.Initialize(credentials, project=project)

PYTHON_VERSION = "".join(platform.python_version_tuple()[0:2])

NAME = f"ppai/geospatial-classification-py{PYTHON_VERSION}"

UUID = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"

TIMEOUT_SEC = 30 * 60  # 30 minutes in seconds
POLL_INTERVAL_SEC = 60  # 1 minute in seconds

VERTEX_AI_SUCCESS_STATE = "PIPELINE_STATE_SUCCEEDED"
VERTEX_AI_FINISHED_STATE = {
    "PIPELINE_STATE_SUCCEEDED",
    "PIPELINE_STATE_FAILED",
    "PIPELINE_STATE_CANCELLED",
}

EARTH_ENGINE_SUCCESS_STATE = "SUCCEEDED"
EARTH_ENGINE_FINISHED_STATE = {"SUCCEEDED"}

BANDS = [
    "B1",
    "B2",
    "B3",
    "B4",
    "B5",
    "B6",
    "B7",
    "B8",
    "B8A",
    "B9",
    "B10",
    "B11",
    "B12",
]
LABEL = "label"

logging.getLogger().setLevel(logging.INFO)


@pytest.fixture(scope="session")
def bucket_name():
    storage_client = storage.Client()

    bucket_name = f"{NAME.replace('/', '-')}-{UUID}"
    bucket = storage_client.create_bucket(bucket_name, location=REGION)

    logging.info(f"bucket_name: {bucket_name}")
    yield bucket_name

    bucket.delete(force=True)


@pytest.fixture(scope="session")
def test_data(bucket_name):
    label_fc = create_label_fc("labeled_geospatial_data.csv")
    label_fc = label_fc.map(format_date)
    data = label_fc.map(get_neighboring_patch).flatten()
    data = data.randomColumn()
    data = data.filter(ee.Filter.gte("random", 0.03))

    training_task = ee.batch.Export.table.toCloudStorage(
        collection=data,
        description="Training image export: test",
        bucket=bucket_name,
        fileNamePrefix="geospatial_training",
        selectors=BANDS + [LABEL],
        fileFormat="TFRecord",
    )

    training_task.start()

    validation_task = ee.batch.Export.table.toCloudStorage(
        collection=data,
        description="Validation image export: test",
        bucket=bucket_name,
        fileNamePrefix="geospatial_validation",
        selectors=BANDS + [LABEL],
        fileFormat="TFRecord",
    )

    validation_task.start()

    train_status = None
    val_status = None

    logging.info("Waiting for data export to complete.")
    for _ in range(0, TIMEOUT_SEC, POLL_INTERVAL_SEC):
        train_status = ee.data.getOperation(training_task.name)["metadata"]["state"]
        val_status = ee.data.getOperation(validation_task.name)["metadata"]["state"]
        if train_status and val_status in EARTH_ENGINE_FINISHED_STATE:
            break
        time.sleep(POLL_INTERVAL_SEC)

    assert train_status == EARTH_ENGINE_SUCCESS_STATE
    assert val_status == EARTH_ENGINE_SUCCESS_STATE
    logging.info(f"Export finished with status {train_status}")

    yield training_task.name


def create_label_fc(path):
    """Creates a FeatureCollection from the label dataframe."""

    dataframe = pd.read_csv(path)
    num_examples = dataframe.shape[0]
    data_dict = dataframe.to_dict()
    feats = []
    properties = ["timestamp", "label"]
    for idx in np.arange(num_examples):
        feat_dict = {}
        geometry = ee.Geometry.Point([data_dict["lon"][idx], data_dict["lat"][idx]])
        for feature in properties:
            feat_dict[feature] = data_dict[feature][idx]
        feat = ee.Feature(geometry, feat_dict)
        feats.append(feat)
    return ee.FeatureCollection(feats)


def format_date(feature):
    """Creates start date and end date properties."""

    # Extract start and end dates
    timestamp = ee.String(feature.get("timestamp")).split(" ").get(0)
    year = ee.Number.parse(ee.String(timestamp).split("-").get(0))
    month = ee.Number.parse(ee.String(timestamp).split("-").get(1))
    day = ee.Number.parse(ee.String(timestamp).split("-").get(2))
    start = ee.Date.fromYMD(year, month, day)
    end = start.advance(1, "day")

    # Create new feature
    feature = feature.set({"start": start, "end": end})

    return feature


def get_neighboring_patch(feature):
    """Gets image pixel values for patch."""

    # filter ImageCollection at start/end dates.
    image = (
        ee.ImageCollection("COPERNICUS/S2")
        .filterDate(feature.get("start"), feature.get("end"))
        .select(BANDS)
        .median()
    )

    # extract pixel values at the lat/lon with a 16x16 padding
    return ee.FeatureCollection(
        [
            image.neighborhoodToArray(ee.Kernel.square(16))
            .sampleRegions(collection=ee.FeatureCollection([feature]), scale=10)
            .first()
        ]
    )


@pytest.fixture(scope="session")
def container_image():
    # https://cloud.google.com/sdk/gcloud/reference/builds/submit
    container_image = f"gcr.io/{PROJECT}/{NAME}:{UUID}"
    subprocess.check_call(
        [
            "gcloud",
            "builds",
            "submit",
            "serving_app",
            f"--tag={container_image}",
            f"--project={PROJECT}",
            "--machine-type=e2-highcpu-8",
            "--timeout=15m",
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
def service_url(bucket_name, container_image):
    # https://cloud.google.com/sdk/gcloud/reference/run/deploy
    service_name = f"{NAME.replace('/', '-')}-{UUID}"
    subprocess.check_call(
        [
            "gcloud",
            "run",
            "deploy",
            service_name,
            f"--image={container_image}",
            "--command=gunicorn",
            "--args=--threads=8,--timeout=0,main:app",
            "--platform=managed",
            f"--project={PROJECT}",
            f"--region={REGION}",
            "--memory=1G",
            f"--set-env-vars=PROJECT={PROJECT}",
            f"--set-env-vars=STORAGE_PATH=gs://{bucket_name}",
            f"--set-env-vars=REGION={REGION}",
            f"--set-env-vars=CONTAINER_IMAGE={container_image}",
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
                "--platform=managed",
                f"--project={PROJECT}",
                f"--region={REGION}",
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
            f"--region={REGION}",
            "--quiet",
        ]
    )


@pytest.fixture(scope="session")
def identity_token():
    yield (
        subprocess.run(
            ["gcloud", "auth", "print-identity-token", f"--project={PROJECT}"],
            capture_output=True,
        )
        .stdout.decode("utf-8")
        .strip()
    )


@pytest.fixture(scope="session")
def train_model(bucket_name):
    aiplatform.init(project=PROJECT, staging_bucket=bucket_name)
    job = aiplatform.CustomTrainingJob(
        display_name="climate_script_colab",
        script_path="task.py",
        container_uri="us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-5:latest",
    )

    model = job.run(args=[f"--bucket={bucket_name}"])
    resource_name = job.resource_name
    logging.info(f"train_model resource_name: {resource_name}")

    # Wait until the model training job finishes.
    status = None
    logging.info("Waiting for model to train.")
    for _ in range(0, TIMEOUT_SEC, POLL_INTERVAL_SEC):
        # https://googleapis.dev/python/aiplatform/latest/aiplatform_v1/job_service.html
        status = job.state.name
        if status in VERTEX_AI_FINISHED_STATE:
            break
        time.sleep(POLL_INTERVAL_SEC)

    logging.info(f"Model job finished with status {status}")
    assert status == VERTEX_AI_SUCCESS_STATE
    yield resource_name


def get_prediction_data(feature, start, end):
    """Extracts Sentinel image as json at specific lat/lon and timestamp."""

    image = (
        ee.ImageCollection("COPERNICUS/S2")
        .filterDate(start, end)
        .select(BANDS)
        .mosaic()
    )

    fc = ee.FeatureCollection(
        [
            image.neighborhoodToArray(ee.Kernel.square(16))
            .sampleRegions(collection=ee.FeatureCollection([feature]), scale=10)
            .first()
        ]
    )

    # download FeatureCollection as JSON
    url = fc.getDownloadURL("geojson")
    bytes = requests.get(url).content
    values = bytes.decode("utf-8")
    json_values = json.loads(values)
    return json_values["features"][0]["properties"]


def test_predict(bucket_name, test_data, train_model, service_url, identity_token):

    # Test point
    plant_location = ee.Feature(ee.Geometry.Point([-84.80529, 39.11613]))
    prediction_data = get_prediction_data(plant_location, "2021-10-01", "2021-10-31")
    logging.info(f"plant location: {plant_location})")

    # Make prediction
    response = requests.post(
        url=f"{service_url}/predict",
        headers={"Authorization": f"Bearer {identity_token}"},
        json={"data": prediction_data, "bucket": bucket_name},
    ).json()

    # Check that we get non-empty predictions.
    assert "predictions" in response["predictions"]
    assert len(response["predictions"]) > 0
