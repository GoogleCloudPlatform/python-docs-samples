# Copyright 2024 Google LLC
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

"""End-to-end tests.

To use an existing bucket, set it without the 'gs://' prefix:
    GOOGLE_CLOUD_BUCKET="my-bucket-name"

Run with `pytest` (local environment):
    # Run all tests.
    PYTHONPATH=.. pytest -s tests/e2e_test.py

    # Run a single test.
    PYTHONPATH=.. pytest -s tests/e2e_test.py -k test_name
"""
try:
    # `conftest` cannot be imported when running in `nox`, but we still
    # try to import it for the autocomplete when writing the tests.
    from conftest import Utils
except ModuleNotFoundError:
    Utils = None

from collections.abc import Callable, Iterator

import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.test_stream import TestStream
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
import conftest  # python-docs-samples/dataflow/conftest.py
import pytest

import custom_model_gemma

DATAFLOW_MACHINE_TYPE = "g2-standard-4"
GEMMA_GCS = "gs://"
NAME = "dataflow/gemma/streaming"

@pytest.fixture(scope="session")
def test_name() -> str:
    # Many fixtures expect a fixture called `test_name`, so be sure to define it!
    return "dataflow/gemma"

@pytest.fixture(scope="session")
def container_image(utils: Utils) -> str:
    yield from utils.cloud_build_submit(NAME)

@pytest.fixture(scope="session")
def messages_topic(pubsub_topic: Callable[[str], str]) -> str:
    return pubsub_topic("messages")


@pytest.fixture(scope="session")
def responses_topic(pubsub_topic: Callable[[str], str]) -> str:
    return pubsub_topic("responses")


@pytest.fixture(scope="session")
def responses_subscription(
    pubsub_subscription: Callable[[str, str], str], responses_topic: str
) -> str:
    return pubsub_subscription("responses", responses_topic)

@pytest.fixture(scope="session")
def dataflow_job(
    project: str,
    bucket_name: str,
    location: str,
    unique_name: str,
    messages_subscription: str,
    responses_topic: str,
) -> Iterator[str]:
    # Copy Gemma onto the local environment
    conftest.run_cmd("gsutil", "cp", GEMMA_GCS, ".")
    # Build the custom container image
    container_name = container_image(Utils)
    # Launch the streaming Dataflow pipeline.
    conftest.run_cmd(
        "python",
        "custom_model_gemma.py",
        f"--messages_subscription={messages_subscription}",
        f"--responses_topic={responses_topic}",
        "--runner=DataflowRunner",
        f"--job_name={unique_name}",
        f"--project={project}",
        f"--temp_location=gs://{bucket_name}/temp",
        f"--region={location}",
        f"--machine_type={DATAFLOW_MACHINE_TYPE}",
        f"--sdk_container_image={container_name}"
        "--requirements_file=requirements.txt",
    )

    # Get the job ID.
    print(f"Finding Dataflow job by name: {unique_name}")
    job_id = conftest.dataflow_find_job_by_name(project, location, unique_name)
    print(f"Dataflow job ID: {job_id}")
    yield job_id

    # Cancel the job as clean up.
    print(f"Cancelling job: {job_id}")
    conftest.dataflow_cancel_job(project, location, job_id)

def test_pipeline_dataflow(
    project: str,
    location: str,
    dataflow_job: str,
    messages_topic: str,
    responses_subscription: str,
) -> None:
    print(f"Waiting for the Dataflow workers to start: {dataflow_job}")
    conftest.wait_until(
        lambda: conftest.dataflow_num_workers(project, location, dataflow_job) > 0,
        "workers are running",
    )
    num_workers = conftest.dataflow_num_workers(project, location, dataflow_job)
    print(f"Dataflow job num_workers: {num_workers}")

    messages = ["This is a test for a Python sample."]
    conftest.pubsub_publish(messages_topic, messages)

    print(f"Waiting for messages on {responses_subscription}")
    responses = conftest.pubsub_wait_for_messages(responses_subscription)
    assert responses, "expected at least one response"