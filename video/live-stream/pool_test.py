# Copyright 2023 Google LLC.
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

import os

import pytest

import get_pool

# import update_pool

project_name = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "us-central1"
pool_id = "default"  # only 1 pool supported per location
peered_network = ""


def test_pool_operations(capsys: pytest.fixture) -> None:
    pool_name_project_id = (
        f"projects/{project_name}/locations/{location}/pools/{pool_id}"
    )

    # All channels must be stopped to update the pool. Pool operations take a
    # long time to complete, so don't run this test on the test network.
    # response = update_pool.update_pool(project_name, location, pool_id, peered_network)
    # assert pool_name_project_id in response.name
    # assert response.network_config.peered_network == peered_network

    response = get_pool.get_pool(project_name, location, pool_id)
    assert pool_name_project_id in response.name
