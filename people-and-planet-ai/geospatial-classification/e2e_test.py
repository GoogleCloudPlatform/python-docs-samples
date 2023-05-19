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

from datetime import datetime, timedelta
import logging
import os
import platform
import subprocess
import time
from typing import NamedTuple
import uuid

import ee
import google.auth
from google.cloud import aiplatform
from google.cloud import storage
import pandas as pd
import pytest
import requests


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
LABEL = "is_powered_on"

IMAGE_COLLECTION = "COPERNICUS/S2"
SCALE = 10

TRAIN_VALIDATION_SPLIT = 0.7

PATCH_SIZE = 16

credentials, _ = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
ee.Initialize(credentials, project=PROJECT)

logging.getLogger().setLevel(logging.INFO)


@pytest.fixture(scope="session")
def bucket_name() -> str:
    storage_client = storage.Client()

    bucket_name = f"{NAME.replace('/', '-')}-{UUID}"
    bucket = storage_client.create_bucket(bucket_name, location=REGION)

    logging.info(f"bucket_name: {bucket_name}")
    yield bucket_name

    bucket.delete(force=True)


@pytest.fixture(scope="session")
def test_data(bucket_name: str) -> str:
    labels_dataframe = pd.read_csv("labeled_geospatial_data.csv")
    train_dataframe = labels_dataframe.sample(
        frac=TRAIN_VALIDATION_SPLIT, random_state=200
    )  # random state is a seed value
    validation_dataframe = labels_dataframe.drop(train_dataframe.index).sample(frac=1.0)

    train_features = [labeled_feature(row) for row in train_dataframe.itertuples()]

    validation_features = [
        labeled_feature(row) for row in validation_dataframe.itertuples()
    ]

    training_task = ee.batch.Export.table.toCloudStorage(
        collection=ee.FeatureCollection(train_features),
        description="Training image export",
        bucket=bucket_name,
        fileNamePrefix="geospatial_training",
        selectors=BANDS + [LABEL],
        fileFormat="TFRecord",
    )

    training_task.start()

    validation_task = ee.batch.Export.table.toCloudStorage(
        collection=ee.FeatureCollection(validation_features),
        description="Validation image export",
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
        if (
            train_status in EARTH_ENGINE_FINISHED_STATE
            and val_status in EARTH_ENGINE_FINISHED_STATE
        ):
            break
        time.sleep(POLL_INTERVAL_SEC)

    assert train_status == EARTH_ENGINE_SUCCESS_STATE
    assert val_status == EARTH_ENGINE_SUCCESS_STATE
    logging.info(f"Export finished with status {train_status}")

    yield training_task.name


def labeled_feature(row: NamedTuple) -> ee.FeatureCollection:
    start = datetime.fromisoformat(row.timestamp)
    end = start + timedelta(days=1)
    image = (
        ee.ImageCollection(IMAGE_COLLECTION)
        .filterDate(start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
        .select(BANDS)
        .mosaic()
    )
    point = ee.Feature(
        ee.Geometry.Point([row.lon, row.lat]),
        {LABEL: row.is_powered_on},
    )
    return (
        image.neighborhoodToArray(ee.Kernel.square(PATCH_SIZE))
        .sampleRegions(ee.FeatureCollection([point]), scale=SCALE)
        .first()
    )


@pytest.fixture(scope="session")
def container_image(bucket_name: str) -> str:
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
def service_url(bucket_name: str, container_image: str) -> str:
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
def train_model(bucket_name: str) -> str:
    aiplatform.init(project=PROJECT, staging_bucket=bucket_name)
    job = aiplatform.CustomTrainingJob(
        display_name="climate_script_colab",
        script_path="task.py",
        container_uri="us-docker.pkg.dev/vertex-ai/training/tf-gpu.2-7:latest",
    )

    job.run(
        accelerator_type="NVIDIA_TESLA_K80",
        accelerator_count=1,
        args=[f"--bucket={bucket_name}"],
    )

    logging.info(f"train_model resource_name: {job.resource_name}")

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
    yield job.resource_name


def get_prediction_data(lon: float, lat: float, start: str, end: str) -> dict:
    """Extracts Sentinel image as json at specific lat/lon and timestamp."""

    location = ee.Feature(ee.Geometry.Point([lon, lat]))
    image = (
        ee.ImageCollection(IMAGE_COLLECTION)
        .filterDate(start, end)
        .select(BANDS)
        .mosaic()
    )

    feature = image.neighborhoodToArray(ee.Kernel.square(PATCH_SIZE)).sampleRegions(
        collection=ee.FeatureCollection([location]), scale=SCALE
    )

    return feature.getInfo()["features"][0]["properties"]


def test_predict(
    bucket_name: str,
    test_data: str,
    train_model: str,
    service_url: str,
    identity_token: str,
) -> None:

    # Test point
    prediction_data = get_prediction_data(
        -84.80529, 39.11613, "2021-10-01", "2021-10-31"
    )

    # Make prediction
    response = requests.post(
        url=f"{service_url}/predict",
        headers={"Authorization": f"Bearer {identity_token}"},
        json={"data": prediction_data, "bucket": bucket_name},
    ).json()

    # Check that we get non-empty predictions.
    assert "predictions" in response["predictions"]
    assert len(response["predictions"]) > 0
