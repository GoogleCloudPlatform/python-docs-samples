#!/usr/bin/env python

# Copyright 2022 Google LLC
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

import subprocess

try:
    # `conftest` cannot be imported when running in `nox`, but we still
    # try to import it for the autocomplete when writing the tests.
    from conftest import Utils
except ModuleNotFoundError:
    Utils = None
import pytest

NAME = "dataflow/custom-containers/ubuntu"


@pytest.fixture(scope="session")
def bucket_name(utils: Utils) -> str:
    yield from utils.storage_bucket(NAME)


@pytest.fixture(scope="session")
def container_image(utils: Utils) -> str:
    yield from utils.cloud_build_submit(image_name=NAME)


def test_tensorflow_minimal(
    utils: Utils, bucket_name: str, container_image: str
) -> None:
    subprocess.check_call(
        [
            "python",
            "main.py",
            "--runner=DataflowRunner",
            f"--project={utils.project}",
            f"--region={utils.region}",
            f"--temp_location=gs://{bucket_name}",
            f"--sdk_container_image={container_image}",
            "--experiment=use_runner_v2",
        ]
    )
