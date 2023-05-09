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

from google.cloud import storage
from googleapiclient.discovery import build
import numpy as np
import pandas as pd
import pytest
import requests

dataflow = build("dataflow", "v1b3")


PYTHON_VERSION = "".join(platform.python_version_tuple()[0:2])

NAME = f"ppai/timeseries-classification-py{PYTHON_VERSION}"

UUID = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"

TIMEOUT_SEC = 30 * 60  # 30 minutes in seconds
POLL_INTERVAL_SEC = 60  # 1 minute in seconds

DATAFLOW_SUCCESS_STATE = "JOB_STATE_DONE"
DATAFLOW_FINISHED_STATE = {
    "JOB_STATE_DONE",
    "JOB_STATE_FAILED",
    "JOB_STATE_CANCELLED",
    "JOB_STATE_DRAINED",
}

VERTEX_AI_SUCCESS_STATE = "JOB_STATE_SUCCEEDED"
VERTEX_AI_FINISHED_STATE = {
    "JOB_STATE_SUCCEEDED",
    "JOB_STATE_FAILED",
    "JOB_STATE_CANCELLED",
}

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
def raw_data_dir(bucket_name: str) -> str:
    storage_client = storage.Client()

    raw_data_dir = "data"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"{raw_data_dir}/56980685061237.npz")
    blob.upload_from_filename("test_data/56980685061237.npz")

    logging.info(f"raw_data_dir: gs://{bucket_name}/{raw_data_dir}")
    yield f"gs://{bucket_name}/{raw_data_dir}"

    blob.delete()


@pytest.fixture(scope="session")
def raw_labels_dir(bucket_name: str) -> str:
    storage_client = storage.Client()

    raw_labels_dir = "labels"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"{raw_labels_dir}/labels.csv")
    blob.upload_from_filename("test_data/labels.csv")

    logging.info(f"raw_labels_dir: gs://{bucket_name}/{raw_labels_dir}")
    yield f"gs://{bucket_name}/{raw_labels_dir}"

    blob.delete()


@pytest.fixture(scope="session")
def container_image() -> str:
    # https://cloud.google.com/sdk/gcloud/reference/builds/submit
    container_image = f"gcr.io/{PROJECT}/{NAME}:{UUID}"
    subprocess.check_call(
        [
            "gcloud",
            "builds",
            "submit",
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
            "--memory=4G",
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
def access_token() -> str:
    yield (
        subprocess.run(
            ["gcloud", "auth", "print-identity-token", f"--project={PROJECT}"],
            capture_output=True,
        )
        .stdout.decode("utf-8")
        .strip()
    )


@pytest.fixture(scope="session")
def create_datasets(
    service_url: str, access_token: str, raw_data_dir: str, raw_labels_dir: str
) -> str:
    raw_response = requests.post(
        f"{service_url}/create-datasets",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "raw_data_dir": raw_data_dir,
            "raw_labels_dir": raw_labels_dir,
        },
    )
    logging.info(f"create_datasets response: {raw_response}")

    response = raw_response.json()
    job_id = response["job_id"]
    job_url = response["job_url"]
    logging.info(f"create_datasets job_id: {job_id}")
    logging.info(f"create_datasets job_url: {job_url}")

    # Wait until the Dataflow job finishes.
    status = None
    logging.info("Waiting for datasets to be created.")
    for _ in range(0, TIMEOUT_SEC, POLL_INTERVAL_SEC):
        # https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.jobs/get
        job = (
            dataflow.projects()
            .jobs()
            .get(
                projectId=PROJECT,
                jobId=job_id,
                view="JOB_VIEW_SUMMARY",
            )
            .execute()
        )

        status = job["currentState"]
        if status in DATAFLOW_FINISHED_STATE:
            break
        time.sleep(POLL_INTERVAL_SEC)

    logging.info(f"Datasets job finished with status {status}")
    assert status == DATAFLOW_SUCCESS_STATE, f"job_url: {job_url}"
    yield job_id


@pytest.fixture(scope="session")
def train_model(service_url: str, access_token: str, create_datasets: str) -> None:
    logging.info("Training model")
    raw_response = requests.post(
        url=f"{service_url}/train-model",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"train_epochs": 10, "batch_size": 8, "sync": True},
    )
    logging.info(f"train_model response: {raw_response}")


def test_predict(service_url: str, access_token: str, train_model: None) -> None:
    with open("test_data/56980685061237.npz", "rb") as f:
        input_data = pd.DataFrame(np.load(f)["x"])

    raw_response = requests.post(
        url=f"{service_url}/predict",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"inputs": input_data.to_dict("list")},
    )
    logging.info(f"predict response: {raw_response}")

    response = raw_response.json()
    predictions = pd.DataFrame(response["predictions"])

    # Check that we get non-empty predictions.
    assert "is_fishing" in predictions
    assert len(predictions["is_fishing"]) > 0
