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

from create_legacy_network import create_legacy_network
from delete_legacy_network import delete_legacy_network
from list_networks import list_networks


@mock.patch("google.cloud.vmwareengine_v1.VmwareEngineClient")
def test_network_create(mock_client_class):
    mock_client = mock_client_class.return_value
    network_mock = (
        mock_client.create_vmware_engine_network.return_value.result.return_value
    )
    network = create_legacy_network("proooject", "around_here")
    assert network is network_mock
    mock_client.create_vmware_engine_network.assert_called_once()
    assert len(mock_client.create_vmware_engine_network.call_args[0]) == 1
    request = mock_client.create_vmware_engine_network.call_args[0][0]
    assert request.parent == "projects/proooject/locations/around_here"
    assert request.vmware_engine_network_id == "around_here-default"
    assert (
        request.vmware_engine_network.type_
        == vmwareengine_v1.VmwareEngineNetwork.Type.LEGACY
    )
    assert (
        request.vmware_engine_network.description
        == "Legacy network created using vmwareengine_v1.VmwareEngineNetwork"
    )


@mock.patch("google.cloud.vmwareengine_v1.VmwareEngineClient")
def test_network_list(mock_client_class):
    mock_client = mock_client_class.return_value
    ret = list_networks("projejejkt", "reggeregion")
    mock_client.list_vmware_engine_networks.assert_called_once_with(
        parent="projects/projejejkt/locations/reggeregion"
    )
    assert ret is mock_client.list_vmware_engine_networks.return_value


@mock.patch("google.cloud.vmwareengine_v1.VmwareEngineClient")
def test_network_delete(mock_client_class):
    mock_client = mock_client_class.return_value
    delete_legacy_network("p1", "r1")
    mock_client.delete_vmware_engine_network.assert_called_once_with(
        name="projects/p1/" "locations/r1/" "vmwareEngineNetworks/r1-default"
    )
