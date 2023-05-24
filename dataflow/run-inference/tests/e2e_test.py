#!/usr/bin/env python

# Copyright 2023 Google LLC
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

Run with `nox` (clean virtual environment):
    nox -s lint
    nox -s py-3.11
"""

from __future__ import annotations

from collections.abc import Callable, Iterator

import conftest  # python-docs-samples/dataflow/conftest.py

from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.test_stream import TestStream
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import is_not_empty
import pytest

import main

MODEL_NAME = "google/flan-t5-small"
MACHINE_TYPE = "n2-standard-2"


@pytest.fixture(scope="session")
def test_name() -> str:
    # Many fixtures expect a fixture called `test_name`, so be sure to define it!
    return "dataflow/run-inference"


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
def state_dict_path() -> str:
    filename = "state_dict.pt"
    print(f"state_dict_path: {filename}")
    conftest.run_cmd(
        "python",
        "load-state-dict.py",
        "local",
        f"--model-name={MODEL_NAME}",
        f"--state-dict-path={filename}",
    )
    return filename


@pytest.fixture(scope="session")
def container_image(project: str, test_name: str, unique_id: str) -> Iterator[str]:
    image_name = f"gcr.io/{project}/{test_name}:{unique_id}"

    # The actual container is created by Dataflow.
    yield image_name

    conftest.run_cmd(
        "gcloud",
        "container",
        "images",
        "delete",
        image_name,
        "--force-delete-tags",
        "--quiet",
    )
    print(f"Deleted image: {image_name}")


@pytest.fixture(scope="session")
def dataflow_job(
    project: str,
    bucket_name: str,
    location: str,
    unique_name: str,
    messages_topic: str,
    responses_topic: str,
    state_dict_path: str,
    container_image: str,
) -> Iterator[str]:
    # Upload the state dict to Cloud Storage.
    state_dict_gcs = f"gs://{bucket_name}/temp/state_dict.pt"
    conftest.run_cmd("gsutil", "cp", "-n", state_dict_path, state_dict_gcs)

    # Launch the streaming Dataflow pipeline.
    conftest.run_cmd(
        "python",
        "main.py",
        f"--messages-topic={messages_topic}",
        f"--responses-topic={responses_topic}",
        f"--model-name={MODEL_NAME}",
        f"--state-dict-path={state_dict_gcs}",
        "--runner=DataflowRunner",
        f"--job_name={unique_name}",
        f"--project={project}",
        f"--temp_location=gs://{bucket_name}/temp",
        f"--region={location}",
        f"--machine_type={MACHINE_TYPE}",
        # f"--sdk_container_image={container_image}",
        "--requirements_file=requirements.txt",
        "--prebuild_sdk_container_engine=cloud_build",
        f"--docker_registry_push_url={container_image}",
        "--sdk_location=container",
    )

    # Get the job ID.
    print(f"Finding Dataflow job by name: {unique_name}")
    job_id = conftest.dataflow_find_job_by_name(project, location, unique_name)
    print(f"Dataflow job ID: {job_id}")
    yield job_id

    # Cancel the job as clean up.
    print(f"Cancelling job: {job_id}")
    conftest.dataflow_cancel_job(project, location, job_id)


def test_load_state_dict_vertex(
    project: str,
    bucket_name: str,
    location: str,
    unique_name: str,
) -> None:
    conftest.run_cmd(
        "python",
        "load-state-dict.py",
        "vertex",
        f"--model-name={MODEL_NAME}",
        f"--state-dict-path=gs://{bucket_name}/temp/state_dict_vertex.pt",
        f"--job-name={unique_name}",
        f"--project={project}",
        f"--bucket={bucket_name}",
        f"--location={location}",
    )


def test_pipeline_local(state_dict_path: str) -> None:
    with TestPipeline() as pipeline:
        responses = (
            pipeline
            | "Create" >> TestStream().add_elements(["Hello!"])
            | "Ask LLM" >> main.AskLanguageModel(MODEL_NAME, state_dict_path)
        )
        assert_that(responses, is_not_empty(), "responses is not empty")


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
