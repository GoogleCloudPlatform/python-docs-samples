# Copyright 2024 Google LLC
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

# This is a test that exercises the example. It is not a part of the example.

try:
    # `conftest` cannot be imported when running in `nox`, but we still
    # try to import it for the autocomplete when writing the tests.
    from conftest import Utils
except ModuleNotFoundError:
    Utils = None
import pytest

NAME = "dataflow/flex-templates/pipeline-with-dependencies"
SDK_IMAGE_NAME = NAME + "/sdk_container_image"
TEMPLATE_IMAGE_NAME = NAME + "/template_image"


@pytest.fixture(scope="session")
def bucket_name(utils: Utils) -> str:
    yield from utils.storage_bucket(NAME)


def _include_repo(utils: Utils, image: str) -> str:
    project = utils.project
    gcr_project = project.replace(":", "/")
    return f"gcr.io/{gcr_project}/{image}"


@pytest.fixture(scope="session")
def sdk_container_image(utils: Utils) -> str:
    yield from utils.cloud_build_submit(SDK_IMAGE_NAME)


@pytest.fixture(scope="session")
def flex_template_path(utils: Utils, bucket_name: str, sdk_container_image: str) -> str:
    yield from utils.dataflow_flex_template_build(bucket_name, sdk_container_image)


@pytest.fixture(scope="session")
def dataflow_job_id(
    utils: Utils, bucket_name: str, flex_template_path: str, sdk_container_image: str
) -> str:
    yield from utils.dataflow_flex_template_run(
        job_name=NAME,
        template_path=flex_template_path,
        bucket_name=bucket_name,
        parameters={
            "input": "gs://dataflow-samples/shakespeare/hamlet.txt",
            "output": f"gs://{bucket_name}/output",
            "sdk_container_image": _include_repo(utils, sdk_container_image),
        },
    )


def test_flex_template_with_dependencies_and_custom_container(
    utils: Utils, dataflow_job_id: str
) -> None:
    utils.dataflow_jobs_wait(dataflow_job_id, target_states={"JOB_STATE_DONE"})
