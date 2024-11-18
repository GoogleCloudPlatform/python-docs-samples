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

# [START vmwareengine_create_private_cloud]
from google.api_core import operation
from google.cloud import vmwareengine_v1

DEFAULT_MANAGEMENT_CIDR = "192.168.0.0/24"
DEFAULT_NODE_COUNT = 3


def create_private_cloud(
    project_id: str, zone: str, network_name: str, cloud_name: str, cluster_name: str
) -> operation.Operation:
    """
    Creates a new Private Cloud using VMware Engine.

    Creating a new Private Cloud is a long-running operation and it may take over an hour.

    Args:
        project_id: name of the project you want to use.
        zone: the zone you want to use, i.e. "us-central1-a"
        network_name: name of the VMWareNetwork to use for the new Private Cloud
        cloud_name: name of the new Private Cloud
        cluster_name: name for the new cluster in this Private Cloud

    Returns:
        An operation object representing the started operation. You can call its .result() method to wait for it to finish.
    """
    request = vmwareengine_v1.CreatePrivateCloudRequest()
    request.parent = f"projects/{project_id}/locations/{zone}"
    request.private_cloud_id = cloud_name

    request.private_cloud = vmwareengine_v1.PrivateCloud()
    request.private_cloud.management_cluster = (
        vmwareengine_v1.PrivateCloud.ManagementCluster()
    )
    request.private_cloud.management_cluster.cluster_id = cluster_name

    node_config = vmwareengine_v1.NodeTypeConfig()
    node_config.node_count = DEFAULT_NODE_COUNT

    # Currently standard-72 is the only supported node type.
    request.private_cloud.management_cluster.node_type_configs = {
        "standard-72": node_config
    }

    request.private_cloud.network_config = vmwareengine_v1.NetworkConfig()
    request.private_cloud.network_config.vmware_engine_network = network_name
    request.private_cloud.network_config.management_cidr = DEFAULT_MANAGEMENT_CIDR

    client = vmwareengine_v1.VmwareEngineClient()
    return client.create_private_cloud(request)


# [END vmwareengine_create_private_cloud]
