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
    cd dataflow/gemma-flex-template

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

from collections.abc import Callable

import conftest  # python-docs-samples/dataflow/conftest.py
from conftest import Utils

import pytest

DATAFLOW_MACHINE_TYPE = "g2-standard-4"
GEMMA_GCS = "gs://perm-dataflow-gemma-example-testdata/pytorch_model"
NAME = "dataflow/gemma-flex-template/streaming"

# There are limited resources in us-central1, so change to a known good region.
REGION = "us-west1"


@pytest.fixture(scope="session")
def test_name() -> str:
    # Many fixtures expect a fixture called `test_name`, so be sure to define it!
    return "dataflow/gemma-flex-template"


@pytest.fixture(scope="session")
def bucket_name(utils: Utils) -> str:
    yield from utils.storage_bucket(NAME)


@pytest.fixture(scope="session")
def messages_topic(pubsub_topic: Callable[[str], str]) -> str:
    return pubsub_topic("messages")


@pytest.fixture(scope="session")
def messages_subscription(
    pubsub_subscription: Callable[[str, str], str], messages_topic: str
) -> str:
    return pubsub_subscription("messages", messages_topic)


@pytest.fixture(scope="session")
def responses_topic(pubsub_topic: Callable[[str], str]) -> str:
    return pubsub_topic("responses")


@pytest.fixture(scope="session")
def responses_subscription(
    pubsub_subscription: Callable[[str, str], str], responses_topic: str
) -> str:
    return pubsub_subscription("responses", responses_topic)


@pytest.fixture(scope="session")
def flex_template_image(utils: Utils) -> str:
    conftest.run_cmd("gsutil", "cp", "-r", GEMMA_GCS, ".")
    yield from utils.cloud_build_submit(NAME)


@pytest.fixture(scope="session")
def flex_template_path(utils: Utils, bucket_name: str, flex_template_image: str) -> str:
    yield from utils.dataflow_flex_template_build(bucket_name, flex_template_image)


@pytest.fixture(scope="session")
def dataflow_job(
    utils: Utils,
    project: str,
    location: str,
    bucket_name: str,
    flex_template_image: str,
    flex_template_path: str,
    messages_subscription: str,
    responses_topic: str,
) -> str:
    yield from utils.dataflow_flex_template_run(
        job_name=NAME,
        template_path=flex_template_path,
        bucket_name=bucket_name,
        project=project,
        region=REGION,
        parameters={
            "messages_subscription": messages_subscription,
            "responses_topic": responses_topic,
            "device": "GPU",
            "sdk_container_image": f"gcr.io/{project}/{flex_template_image}",
            "machine_type": f"{DATAFLOW_MACHINE_TYPE}",
            "disk_size_gb": "50",
        },
        additional_experiments={
            "worker_accelerator": "type:nvidia-l4;count:1;install-nvidia-driver",
        },
    )


@pytest.mark.timeout(5400)
def test_pipeline_dataflow(
    project: str,
    location: str,
    dataflow_job: str,
    messages_topic: str,
    responses_subscription: str,
) -> None:
    print(f"Waiting for the Dataflow workers to start: {dataflow_job}")
    conftest.wait_until(
        lambda: conftest.dataflow_num_workers(project, REGION, dataflow_job) > 0,
        "workers are running",
    )
    num_workers = conftest.dataflow_num_workers(project, REGION, dataflow_job)
    print(f"Dataflow job num_workers: {num_workers}")

    messages = ["This is a test for a Python sample."]
    conftest.pubsub_publish(messages_topic, messages)

    print(f"Waiting for messages on {responses_subscription}")
    responses = conftest.pubsub_wait_for_messages(responses_subscription)

    print(f"Received {len(responses)} responses(s)")

    for msg in responses:
        print(f"- {type(msg)} - {msg}")

    assert responses, "expected at least one response"
