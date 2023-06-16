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

from google.api_core import operation
from google.cloud import vmwareengine_v1


def create_cluster(
    project_id: str,
    zone: str,
    private_cloud_name: str,
    cluster_name: str,
    node_count: int = 4,
) -> operation.Operation:
    """
    Create a new cluster in a private cloud.

    Creation of a new cluster is a slow operation. Might take well over 15 minutes.

    Args:
        project_id: name of the project you want to use.
        zone: region in which your private cloud is located.
        private_cloud_name: name of the private cloud hosting the new cluster.
        cluster_name: name of the new cluster.
        node_count: number of nodes in the new cluster.

    Returns:
        An Operation object related to started cluster creation operation.
    """
    if node_count < 3:
        raise RuntimeError("Cluster needs to have at least 3 nodes")

    client = vmwareengine_v1.VmwareEngineClient()
    request = vmwareengine_v1.CreateClusterRequest()
    request.parent = (
        f"projects/{project_id}/locations/{zone}/privateClouds/{private_cloud_name}"
    )

    request.cluster = vmwareengine_v1.Cluster()
    request.cluster.name = cluster_name

    request.cluster.node_type_configs = {
        "standard-72": vmwareengine_v1.NodeTypeConfig()
    }
    request.cluster.node_type_configs["standard-72"].node_count = node_count

    return client.create_cluster(request)
