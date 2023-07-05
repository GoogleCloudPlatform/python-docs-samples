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

from unittest import mock

from google.cloud import vmwareengine_v1
import pytest

from create_policy import create_network_policy
from delete_policy import delete_network_policy
from update_policy import update_network_policy


@mock.patch("google.cloud.vmwareengine_v1.VmwareEngineClient")
def test_create_policy(mock_client_class):
    mock_client = mock_client_class.return_value

    create_network_policy("pro", "reg", "1.2.3.4/26", False, True)

    mock_client.create_network_policy.assert_called_once()
    assert len(mock_client.create_network_policy.call_args[0]) == 1
    request = mock_client.create_network_policy.call_args[0][0]
    assert isinstance(request, vmwareengine_v1.CreateNetworkPolicyRequest)
    assert request.parent == "projects/pro/locations/reg"
    assert request.network_policy.edge_services_cidr == "1.2.3.4/26"
    assert request.network_policy.external_ip.enabled is True
    assert request.network_policy.internet_access.enabled is False


@mock.patch("google.cloud.vmwareengine_v1.VmwareEngineClient")
def test_create_policy_value_error(mock_client_class):
    with pytest.raises(ValueError):
        create_network_policy("pro", "reg", "1.2.3.4/24", False, False)


@mock.patch("google.cloud.vmwareengine_v1.VmwareEngineClient")
def test_delete_policy(mock_client_class):
    mock_client = mock_client_class.return_value

    delete_network_policy("projakt", "regiom")

    mock_client.delete_network_policy.assert_called_once()
    assert len(mock_client.delete_network_policy.call_args[0]) == 0
    assert len(mock_client.delete_network_policy.call_args[1]) == 1
    name = mock_client.delete_network_policy.call_args[1]["name"]
    assert name == "projects/projakt/locations/regiom/networkPolicies/regiom-default"


@mock.patch("google.cloud.vmwareengine_v1.VmwareEngineClient")
def test_update_policy(mock_client_class):
    mock_client = mock_client_class.return_value

    update_network_policy("project", "regiono", True, False)

    mock_client.update_network_policy.assert_called_once()
    assert len(mock_client.update_network_policy.call_args[0]) == 1
    request = mock_client.update_network_policy.call_args[0][0]
    assert isinstance(request, vmwareengine_v1.UpdateNetworkPolicyRequest)
    assert (
        request.network_policy.name
        == "projects/project/locations/regiono/networkPolicies/regiono-default"
    )
    assert request.network_policy.external_ip.enabled is False
    assert request.network_policy.internet_access.enabled is True
