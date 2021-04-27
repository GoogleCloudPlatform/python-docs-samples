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

import conftest as utils
import pytest

NAME = "dataflow-flex-templates-streaming-beam"


@pytest.fixture(scope="session")
def bucket_name() -> str:
    return utils.storage_bucket(NAME)


@pytest.fixture(scope="session")
def pubsub_topic() -> str:
    return utils.pubsub_topic(NAME)


@pytest.fixture(scope="session")
def pubsub_subscription(pubsub_topic: str) -> str:
    return utils.pubsub_subscription(pubsub_topic, NAME)


@pytest.fixture(scope="session")
def bigquery_dataset() -> str:
    return utils.bigquery_dataset(NAME.replace("-", "_"))


@pytest.fixture(scope="session")
def pubsub_publisher(pubsub_topic: str) -> bool:
    return utils.pubsub_publisher(
        pubsub_topic,
        new_msg=lambda i: json.dumps(
            {
                "url": "https://beam.apache.org/",
                "review": "positive" if i % 2 == 0 else "negative",
            }
        ),
    )


@pytest.fixture(scope="session")
def flex_template_image() -> str:
    return utils.container_image(NAME)


@pytest.fixture(scope="session")
def flex_template_path(bucket_name: str, flex_template_image: str) -> str:
    return utils.dataflow_flex_template_build(
        bucket_name=bucket_name,
        template_image=flex_template_image,
        metadata_file="metadata.json",
    )


def test_run_template(
    bucket_name: str,
    pubsub_publisher: str,
    pubsub_subscription: str,
    flex_template_path: str,
    bigquery_dataset: str,
) -> None:

    bigquery_table = "output_table"
    job_name = utils.dataflow_flex_template_run(
        job_name=NAME,
        template_path=flex_template_path,
        bucket_name=bucket_name,
        parameters={
            "input_subscription": pubsub_subscription,
            "output_table": f"{bigquery_dataset}.{bigquery_table}",
        },
    )

    # Since this is a streaming job, it will never finish running.
    # Wait for 10 minutes, and then cancel the job.
    time.sleep(10 * 60)
    utils.dataflow_jobs_cancel(job_name)

    # Check for output data in BigQuery.
    query = f"SELECT * FROM {bigquery_dataset.replace(':', '.')}.{bigquery_table}"
    rows = list(utils.bigquery_query(query))
    assert len(rows) > 0
    for row in rows:
        assert "score" in row
