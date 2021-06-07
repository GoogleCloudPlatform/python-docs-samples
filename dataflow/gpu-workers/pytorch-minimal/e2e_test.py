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
import pytest

NAME = "dataflow-gpu-pytorch"


@pytest.fixture(scope="session")
def bucket_name(utils: Utils) -> str:
    yield from utils.storage_bucket(NAME)


@pytest.fixture(scope="session")
def worker_image(utils: Utils) -> str:
    yield from utils.cloud_build_submit(NAME, config="build.yaml")


def test_end_to_end(utils: Utils, bucket_name: str, worker_image: str) -> None:
    # Run the Beam pipeline in Dataflow making sure GPUs are used.
    utils.cloud_build_submit(
        config="run.yaml",
        substitutions={"_TEMP_LOCATION": f"gs://{bucket_name}/temp"},
    )
