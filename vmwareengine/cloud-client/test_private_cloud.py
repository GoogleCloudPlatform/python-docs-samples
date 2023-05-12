# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import uuid

import pytest

import google.auth

from create_legacy_network import create_legacy_network
from create_private_cloud import create_private_cloud
from delete_legacy_network import delete_legacy_network
from delete_private_cloud import delete_private_cloud_by_name
from list_networks import list_networks

PROJECT = google.auth.default()[1]
REGION = 'asia-northeast1'

@pytest.fixture
def legacy_network():
    for network in list_networks(PROJECT, REGION):
        if network.name == f"projects/{PROJECT}/locations/{REGION}/vmwareEngineNetworks/{REGION}-default":
            yield network
            # We don't want to delete a network that's already there
            break
    else:
        yield create_legacy_network(PROJECT, REGION)
        delete_legacy_network(PROJECT, REGION)


def test_private_cloud_crud(legacy_network):
    cloud_name = "test-cloud-" + uuid.uuid4().hex[:6]
    cloud = create_private_cloud(PROJECT, f'{REGION}-a', legacy_network.name, cloud_name, "management-cluster")
    delete_private_cloud_by_name(cloud.name)
