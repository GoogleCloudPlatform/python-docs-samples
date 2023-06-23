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
from unittest import mock
import pytest

import google.auth

from create_legacy_network import create_legacy_network
from create_private_cloud import create_private_cloud
from delete_legacy_network import delete_legacy_network
from delete_private_cloud import delete_private_cloud_by_full_name
from list_networks import list_networks


@mock.patch('google.cloud.vmwareengine_v1.VmwareEngineClient')
def test_private_cloud_create(mock_client_class):
    mock_client = mock_client_class.return_value
    cloud_name = "test-cloud-" + uuid.uuid4().hex[:6]
    region = "rege"
    create_private_cloud(
        "projekto", "regiono", "networko", cloud_name, "management-cluster"
    )

    mock_client.create_private_cloud.assert_called_once()
    assert len(mock_client.create_private_cloud.call_args.args) == 1
    assert len(mock_client.create_private_cloud.call_args.kwargs) == 0
    request = mock_client.create_private_cloud.call_args.args[0]

    assert request.private_cloud.management_cluster.cluster_id == "management-cluster"
    assert request.parent == f"projects/projekto/locations/regiono"
    assert request.private_cloud.network_config.vmware_engine_network == "networko"


@mock.patch('google.cloud.vmwareengine_v1.VmwareEngineClient')
def test_delete_cloud_create(mock_client_class):
    mock_client = mock_client_class.return_value

    delete_private_cloud_by_full_name("the_full_name_of_the_cloud")

    mock_client.delete_private_cloud.assert_called_once()
    assert len(mock_client.delete_private_cloud.call_args.args) == 1
    assert len(mock_client.delete_private_cloud.call_args.kwargs) == 0
    request = mock_client.delete_private_cloud.call_args.args[0]
    assert request.name == "the_full_name_of_the_cloud"