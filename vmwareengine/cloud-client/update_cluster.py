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

# [START vmwareengine_update_cluster_node_count]
from google.api_core import operation
from google.cloud import vmwareengine_v1


def update_cluster_node_count(
    project_id: str,
    zone: str,
    private_cloud_name: str,
    cluster_name: str,
    node_count: int,
) -> operation.Operation:
    """
    Modify the number of nodes in a cluster in a private cloud.

    Modifying a cluster is a long-running operation and it may take over an hour.

    Args:
        project_id: name of the project you want to use.
        zone: zone in which your private cloud is located.
        private_cloud_name: name of the private cloud hosting the cluster.
        cluster_name: name of the cluster.
        node_count: desired number of nodes in the cluster.

    Returns:
        An Operation object related to cluster modification operation.
    """
    if node_count < 3:
        raise RuntimeError("Cluster needs to have at least 3 nodes")
    client = vmwareengine_v1.VmwareEngineClient()
    request = vmwareengine_v1.UpdateClusterRequest()
    request.cluster = vmwareengine_v1.Cluster()
    request.cluster.name = (
        f"projects/{project_id}/locations/{zone}/privateClouds/{private_cloud_name}"
        f"/clusters/{cluster_name}"
    )
    request.cluster.node_type_configs = {
        "standard-72": vmwareengine_v1.NodeTypeConfig()
    }
    request.cluster.node_type_configs["standard-72"].node_count = node_count
    request.update_mask = "nodeTypeConfigs.*.nodeCount"
    return client.update_cluster(request)


# [END vmwareengine_update_cluster_node_count]
