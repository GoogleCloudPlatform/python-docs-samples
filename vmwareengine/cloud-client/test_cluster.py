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

from create_cluster import create_cluster
from create_custom_cluster import create_custom_cluster
from delete_cluster import delete_cluster
from update_cluster import update_cluster_node_count


@mock.patch("google.cloud.vmwareengine_v1.VmwareEngineClient")
def test_create_cluster(mock_client_class):
    mock_client = mock_client_class.return_value

    create_cluster("project11", "zone43", "my-cloud", "my-cluuuster", 99)

    mock_client.create_cluster.assert_called_once()
    assert len(mock_client.create_cluster.call_args[0]) == 1
    assert len(mock_client.create_cluster.call_args[1]) == 0
    request = mock_client.create_cluster.call_args[0][0]
    assert isinstance(request, vmwareengine_v1.CreateClusterRequest)
    assert (
        request.parent == "projects/project11/locations/zone43/privateClouds/my-cloud"
    )
    assert request.cluster.name == "my-cluuuster"
    assert request.cluster.node_type_configs["standard-72"].node_count == 99


def test_create_cluster_value_error():
    with pytest.raises(ValueError):
        create_cluster("bad_project", "badzone", "bad_cloud", "bad_cluster", 2)


@mock.patch("google.cloud.vmwareengine_v1.VmwareEngineClient")
def test_create_custom_cluster(mock_client_class):
    mock_client = mock_client_class.return_value

    create_custom_cluster("project121", "zone433", "my_cloud", "my_cluuuster", 98, 7)

    mock_client.create_cluster.assert_called_once()
    assert len(mock_client.create_cluster.call_args[0]) == 1
    assert len(mock_client.create_cluster.call_args[1]) == 0
    request = mock_client.create_cluster.call_args[0][0]
    assert isinstance(request, vmwareengine_v1.CreateClusterRequest)
    assert (
        request.parent == "projects/project121/locations/zone433/privateClouds/my_cloud"
    )
    assert request.cluster.name == "my_cluuuster"
    assert request.cluster.node_type_configs["standard-72"].node_count == 98
    assert request.cluster.node_type_configs["standard-72"].custom_core_count == 7


def test_create_custom_cluster_value_error():
    with pytest.raises(ValueError):
        create_custom_cluster(
            "bad_project", "badzone", "bad_cloud", "bad_cluster", 2, 3
        )


@mock.patch("google.cloud.vmwareengine_v1.VmwareEngineClient")
def test_delete_cluster(mock_client_class):
    mock_client = mock_client_class.return_value

    delete_cluster("projojo", "zona-2", "my_cloud<3", "the_clusterino")

    mock_client.delete_cluster.assert_called_once()
    assert len(mock_client.delete_cluster.call_args[0]) == 1
    assert len(mock_client.delete_cluster.call_args[1]) == 0
    request = mock_client.delete_cluster.call_args[0][0]
    assert isinstance(request, vmwareengine_v1.DeleteClusterRequest)
    assert (
        request.name
        == "projects/projojo/locations/zona-2/privateClouds/my_cloud<3/clusters/the_clusterino"
    )


@mock.patch("google.cloud.vmwareengine_v1.VmwareEngineClient")
def test_update_cluster(mock_client_class):
    mock_client = mock_client_class.return_value

    update_cluster_node_count("projojo", "zona-2", "my_cloud<3", "the_clusterino", 66)

    mock_client.update_cluster.assert_called_once()
    assert len(mock_client.update_cluster.call_args[0]) == 1
    assert len(mock_client.update_cluster.call_args[1]) == 0
    request = mock_client.update_cluster.call_args[0][0]
    assert isinstance(request, vmwareengine_v1.UpdateClusterRequest)
    assert (
        request.cluster.name
        == "projects/projojo/locations/zona-2/privateClouds/my_cloud<3/clusters/the_clusterino"
    )
    assert request.cluster.node_type_configs["standard-72"].node_count == 66
