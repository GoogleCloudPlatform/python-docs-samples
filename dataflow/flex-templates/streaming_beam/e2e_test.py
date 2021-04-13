# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import os
import subprocess
import time
import uuid

from google.cloud import bigquery
import pytest

from .. import testing_utils


SUFFIX = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BUCKET_NAME = f"flex-templates-streaming-beam-{SUFFIX}"
BIGQUERY_DATASET = f"flex_templates_{SUFFIX}"
BIGQUERY_TABLE = "streaming_beam"
TOPIC = f"flex-templates-streaming-beam-{SUFFIX}"
SUBSCRIPTION = TOPIC
IMAGE_NAME = f"gcr.io/{PROJECT}/dataflow/flex-templates/streaming-beam-{SUFFIX}:latest"
TEMPLATE_FILE = "template.json"
REGION = "us-central1"


@pytest.fixture(scope="session")
def bucket_name() -> str:
    return testing_utils.storage_bucket(BUCKET_NAME)


@pytest.fixture(scope="session")
def topic_path() -> str:
    return testing_utils.pubsub_topic(PROJECT, TOPIC)


@pytest.fixture(scope="session")
def subscription_path(topic_path: str) -> str:
    return testing_utils.pubsub_subscription(PROJECT, topic_path, SUBSCRIPTION)


@pytest.fixture(scope="session")
def bigquery_dataset() -> str:
    return testing_utils.bigquery_dataset(PROJECT, BIGQUERY_DATASET)


@pytest.fixture(scope="session")
def publisher(topic_path: str) -> bool:
    return testing_utils.pubsub_publisher(topic_path)


@pytest.fixture(scope="session")
def template_image() -> str:
    return testing_utils.container_image(PROJECT, IMAGE_NAME)


@pytest.fixture(scope="session")
def template_path(bucket_name: str, template_image: str) -> str:
    return testing_utils.dataflow_flex_template_build(
        bucket_name=bucket_name,
        template_file=TEMPLATE_FILE,
        template_image=template_image,
        metadata_file="metadata.json",
    )


def test_run_template(
    publisher: str,
    bucket_name: str,
    template_path: str,
    dataset: str,
    subscription_path: str,
) -> None:

    job_name = f"flex-templates-streaming-beam-{SUFFIX}"
    subprocess.call(
        [
            "gcloud",
            "dataflow",
            "flex-template",
            "run",
            job_name,
            f"--template-file-gcs-location={template_path}",
            f"--temp_location=gs://{bucket_name}/temp",
            f"--parameters=input_subscription={subscription_path}",
            f"--parameters=output_table={dataset}.{BIGQUERY_TABLE}",
            f"--region={REGION}",
        ],
        check=True,
    )

    # Wait for 10 minutes, and then cancel the job.
    time.sleep(10 * 60)
    testing_utils.dataflow_jobs_cancel(PROJECT, job_name)

    # Check for output data in BigQuery.
    bigquery_client = bigquery.Client()
    query = f"SELECT * FROM {PROJECT}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}"
    query_job = bigquery_client.query(query)
    rows = query_job.result()
    assert rows.total_rows > 0
    for row in rows:
        assert row["score"] == 1
