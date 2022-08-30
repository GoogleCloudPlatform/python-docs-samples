# Copyright 2022 Google LLC
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

import json
import os
import time

from google.cloud import bigquery
from google.cloud import pubsub
from google.cloud import storage

try:
    # `conftest` cannot be imported when running in `nox`, but we still
    # try to import it for the autocomplete when writing the tests.
    from conftest import Utils
except ModuleNotFoundError:
    Utils = None
import pytest

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]

NAME = "dataflow/extensible-template"

BQ_TABLE = "ratings"


@pytest.fixture(scope="session")
def bucket_name(utils: Utils) -> str:
    yield from utils.storage_bucket(NAME)


@pytest.fixture(scope="session")
def pubsub_topic(utils: Utils) -> str:
    yield from utils.pubsub_topic(NAME)


@pytest.fixture(scope="session")
def bq_dataset(utils: Utils) -> str:
    yield from utils.bigquery_dataset(NAME)


@pytest.fixture(scope="session")
def bq_table(utils: Utils, bq_dataset: str) -> str:
    yield from utils.bigquery_table(
        bq_dataset,
        BQ_TABLE,
        schema=[
            bigquery.SchemaField("url", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("review", "STRING", mode="REQUIRED"),
        ],
    )


@pytest.fixture(scope="session")
def dataflow_job_id(
    utils: Utils,
    bucket_name: str,
    pubsub_topic: str,
    bq_dataset: str,
    bq_table: str,
) -> str:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob("js/dataflow_udf_transform.js")
    blob.upload_from_filename(os.path.join(os.getcwd(), "dataflow_udf_transform.js"))
    output_table = f"{PROJECT}:{bq_dataset}.{bq_table}"
    yield from utils.dataflow_extensible_template_run(
        job_name=NAME,
        template_path="gs://dataflow-templates/latest/PubSub_to_BigQuery",
        bucket_name=bucket_name,
        parameters={
            "inputTopic": pubsub_topic,
            "outputTableSpec": output_table,
            "javascriptTextTransformGcsPath": f"gs://{bucket_name}/js/dataflow_udf_transform.js",
            "javascriptTextTransformFunctionName": "process",
        },
    )


def test_extensible_template(
    utils: Utils,
    pubsub_topic: str,
    dataflow_job_id: str,
    bq_dataset: str,
    bq_table: str,
) -> None:
    publisher_client = pubsub.PublisherClient()
    for i in range(30):
        good_msg = json.dumps(
            {
                "url": "https://beam.apache.org/",
                "review": "positive" if i % 2 == 0 else "negative",
            }
        )
        publisher_client.publish(pubsub_topic, good_msg.encode("utf-8"))
        bad_msg = json.dumps(
            {
                "url": "https://kafka.apache.org/",
                "review": "positive" if i % 2 == 0 else "negative",
            }
        )
        publisher_client.publish(pubsub_topic, bad_msg.encode("utf-8"))
        time.sleep(10)

    # Wait until the dataflow job starts running successfully.
    # The job is cancelled as part of the teardown to avoid leaking resource.
    utils.dataflow_jobs_wait(
        dataflow_job_id,
        target_states={"JOB_STATE_RUNNING"},
        timeout_sec=300,
        poll_interval_sec=30,
    )

    query = f"SELECT * FROM `{PROJECT}.{bq_dataset}.{bq_table}`"
    good_records = utils.bigquery_query(query)
    assert len(list(good_records)) > 0

    query = f"SELECT * FROM `{PROJECT}.{bq_dataset}.{bq_table}_error_records`"
    bad_records = utils.bigquery_query(query)
    assert len(list(bad_records)) > 0
