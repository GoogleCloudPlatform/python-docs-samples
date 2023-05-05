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


import pytest

import google.auth

from create_legacy_network import create_legacy_network
from delete_legacy_network import delete_legacy_network
from list_networks import list_networks

PROJECT = google.auth.default()[1]
TEST_REGION = 'us-central1'


def test_network_lifecycle():
    for nl in list_networks(PROJECT, TEST_REGION):
        if nl.name == "projects/mestiv-playground/locations/us-central1/vmwareEngineNetworks/us-central1-default":
            pytest.fail(f"Can't run the test. The Legacy network in {TEST_REGION} already exists.")

    network = create_legacy_network(PROJECT, TEST_REGION)

    for nl in list_networks(PROJECT, TEST_REGION):
        if nl.name == network.name:
            break
    else:
        pytest.fail(f"The newly created network {network.name} wasn't found on the network list.")

    delete_legacy_network(PROJECT, TEST_REGION)

    for nl in list_networks(PROJECT, TEST_REGION):
        if nl.name == network.name:
            pytest.fail("The test network should have been deleted at this point.")
