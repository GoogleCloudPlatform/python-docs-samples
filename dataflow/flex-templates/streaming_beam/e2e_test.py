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

import json
import time

try:
    # `conftest` cannot be imported when running in `nox`, but we still
    # try to import it for the autocomplete when writing the tests.
    from conftest import Utils
except ModuleNotFoundError:
    Utils = None
import pytest

NAME = "dataflow/flex-templates/streaming-beam"


@pytest.fixture(scope="session")
def bucket_name(utils: Utils) -> str:
    yield from utils.storage_bucket(NAME)


@pytest.fixture(scope="session")
def pubsub_topic(utils: Utils) -> str:
    yield from utils.pubsub_topic(NAME)


@pytest.fixture(scope="session")
def pubsub_subscription(utils: Utils, pubsub_topic: str) -> str:
    yield from utils.pubsub_subscription(pubsub_topic, NAME)


@pytest.fixture(scope="session")
def pubsub_publisher(utils: Utils, pubsub_topic: str) -> bool:
    yield from utils.pubsub_publisher(
        pubsub_topic,
        new_msg=lambda i: json.dumps(
            {
                "url": "https://beam.apache.org/",
                "review": "positive" if i % 2 == 0 else "negative",
            }
        ),
    )


@pytest.fixture(scope="session")
def bigquery_dataset(utils: Utils) -> str:
    yield from utils.bigquery_dataset(NAME)


@pytest.fixture(scope="session")
def flex_template_image(utils: Utils) -> str:
    yield from utils.cloud_build_submit(NAME)


@pytest.fixture(scope="session")
def flex_template_path(utils: Utils, bucket_name: str, flex_template_image: str) -> str:
    yield from utils.dataflow_flex_template_build(bucket_name, flex_template_image)


def test_flex_template_streaming_beam(
    utils: Utils,
    bucket_name: str,
    pubsub_publisher: str,
    pubsub_subscription: str,
    flex_template_path: str,
    bigquery_dataset: str,
) -> None:

    bigquery_table = "output_table"
    job_id = utils.dataflow_flex_template_run(
        job_name=NAME,
        template_path=flex_template_path,
        bucket_name=bucket_name,
        parameters={
            "input_subscription": pubsub_subscription,
            "output_table": f"{bigquery_dataset}.{bigquery_table}",
        },
    )

    # Since this is a streaming job, it will never finish running.
    # First, lets wait until the job is running.
    utils.dataflow_jobs_wait(job_id, until_status="JOB_STATE_RUNNING")

    # Then, wait 3 minutes for data to arrive, get processed, and cancel it.
    time.sleep(3 * 60)
    utils.dataflow_jobs_cancel(job_id, drain=True)

    # Check for the output data in BigQuery.
    query = f"SELECT * FROM {bigquery_dataset.replace(':', '.')}.{bigquery_table}"
    rows = list(utils.bigquery_query(query))
    assert len(rows) > 0
    for row in rows:
        assert "score" in row
