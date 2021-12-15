#!/usr/bin/env python

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

try:
    # `conftest` cannot be imported when running in `nox`, but we still
    # try to import it for the autocomplete when writing the tests.
    from conftest import Utils
except ModuleNotFoundError:
    Utils = None
from google.cloud import storage
import pytest

NAME = "dataflow/gpu-examples/tensorflow-landsat"


@pytest.fixture(scope="session")
def bucket_name(utils: Utils) -> str:
    yield from utils.storage_bucket(NAME)


@pytest.fixture(scope="session")
def build_image(utils: Utils) -> str:
    yield from utils.cloud_build_submit(
        image_name=NAME,
        config="build.yaml",
        substitutions={"_IMAGE": f"{NAME}:{utils.uuid}"},
    )


@pytest.fixture(scope="session")
def run_dataflow_job(utils: Utils, bucket_name: str, build_image: str) -> str:
    # Run the Beam pipeline in Dataflow making sure GPUs are used.
    yield from utils.cloud_build_submit(
        config="run.yaml",
        substitutions={
            "_JOB_NAME": utils.hyphen_name(NAME),
            "_IMAGE": f"{NAME}:{utils.uuid}",
            "_TEMP_LOCATION": f"gs://{bucket_name}/temp",
            "_REGION": utils.region,
            "_OUTPUT_PATH": f"gs://{bucket_name}/outputs/",
        },
        source="--no-source",
    )


def test_tensorflow_landsat(
    utils: Utils, bucket_name: str, run_dataflow_job: str
) -> None:
    # Wait until the job finishes.
    timeout = 30 * 60  # 30 minutes
    status = utils.dataflow_jobs_wait(
        job_name=utils.hyphen_name(NAME), timeout_sec=timeout
    )
    assert status == "JOB_STATE_DONE", f"Dataflow pipeline finished in {status} status"

    # Check that output files were created and are not empty.
    storage_client = storage.Client()
    print(f">> Checking for output files in: gs://{bucket_name}/outputs/")
    output_files = list(storage_client.list_blobs(bucket_name, prefix="outputs/"))
    assert len(output_files) > 0, f"No files found in gs://{bucket_name}/outputs/"
    for output_file in output_files:
        assert output_file.size > 0, f"Output file is empty: {output_file.name}"
