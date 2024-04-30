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

1. Set your project.
    export GOOGLE_CLOUD_PROJECT="my-project-id"

2. To use an existing bucket, set it without the 'gs://' prefix.
    export GOOGLE_CLOUD_BUCKET="my-bucket-name"

3. Change directory to the sample location.
    cd dataflow/gemma

4. Set the PYTHONPATH to where the conftest is located.
    export PYTHONPATH=..

OPTION A: Run tests with pytest, you can use -k to run specific tests
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt -r requirements-test.txt
    pip check
    python -m pytest --verbose -s

OPTION B: Run tests with nox
    pip install nox
    nox -s py-3.10

NOTE: For the tests to find the conftest in the testing infrastructure,
      add the PYTHONPATH to the "env" in your noxfile_config.py file.
"""
from collections.abc import Callable, Iterator

import conftest  # python-docs-samples/dataflow/conftest.py
from conftest import Utils

import pytest

DATAFLOW_MACHINE_TYPE = "g2-standard-4"
GEMMA_GCS = "gs://perm-dataflow-gemma-example-testdata/gemma_2b"
NAME = "dataflow/gemma/streaming"


@pytest.fixture(scope="session")
def test_name() -> str:
    # Many fixtures expect a fixture called `test_name`, so be sure to define it!
    return "dataflow/gemma"


@pytest.fixture(scope="session")
def container_image(utils: Utils) -> str:
    # Copy Gemma onto the local environment
    conftest.run_cmd("gsutil", "cp", "-r", GEMMA_GCS, ".")
    yield from utils.cloud_build_submit(NAME)


@pytest.fixture(scope="session")
def messages_topic(pubsub_topic: Callable[[str], str]) -> str:
    return pubsub_topic("messages")


@pytest.fixture(scope="session")
def messages_subscription(pubsub_subscription: Callable[[str, str], str],
                          messages_topic: str) -> str:
    return pubsub_subscription("messages", messages_topic)


@pytest.fixture(scope="session")
def responses_topic(pubsub_topic: Callable[[str], str]) -> str:
    return pubsub_topic("responses")


@pytest.fixture(scope="session")
def responses_subscription(pubsub_subscription: Callable[[str, str], str],
                           responses_topic: str) -> str:
    return pubsub_subscription("responses", responses_topic)


@pytest.fixture(scope="session")
def dataflow_job(
        project: str,
        bucket_name: str,
        location: str,
        unique_name: str,
        container_image: str,
        messages_subscription: str,
        responses_topic: str,
) -> Iterator[str]:
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
        f"--sdk_container_image=gcr.io/{project}/{container_image}",
        "--dataflow_service_options=worker_accelerator=type:nvidia-l4;count:1;install-nvidia-driver:5xx",
        "--requirements_cache=skip",
        "--save_main_session",
    )

    # Get the job ID.
    print(f"Finding Dataflow job by name: {unique_name}")
    job_id = conftest.dataflow_find_job_by_name(project, location, unique_name)
    print(f"Dataflow job ID: {job_id}")
    yield job_id

    # Cancel the job as clean up.
    print(f"Cancelling job: {job_id}")
    conftest.dataflow_cancel_job(project, location, job_id)


@pytest.mark.timeout(3600)
def test_pipeline_dataflow(
        project: str,
        location: str,
        dataflow_job: str,
        messages_topic: str,
        responses_subscription: str,
) -> None:
    print(f"Waiting for the Dataflow workers to start: {dataflow_job}")
    conftest.wait_until(
        lambda: conftest.dataflow_num_workers(project, location, dataflow_job)
        > 0,
        "workers are running",
    )
    num_workers = conftest.dataflow_num_workers(project, location,
                                                dataflow_job)
    print(f"Dataflow job num_workers: {num_workers}")

    messages = ["This is a test for a Python sample."]
    conftest.pubsub_publish(messages_topic, messages)

    print(f"Waiting for messages on {responses_subscription}")
    responses = conftest.pubsub_wait_for_messages(responses_subscription)
    assert responses, "expected at least one response"
