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

# [START vmwareengine_delete_cluster]
from google.api_core import operation
from google.cloud import vmwareengine_v1


def delete_cluster(
    project_id: str, zone: str, private_cloud_name: str, cluster_name: str
) -> operation.Operation:
    """
    Delete a cluster from private cloud.

    Deleting a cluster is a long-running operation and it may take over an hour..

    Args:
        project_id: name of the project you want to use.
        zone: region in which your private cloud is located.
        private_cloud_name: name of the private cloud hosting the new cluster.
        cluster_name: name of the new cluster.

    Returns:
        An Operation object related to started cluster deletion operation.
    """
    client = vmwareengine_v1.VmwareEngineClient()
    request = vmwareengine_v1.DeleteClusterRequest()
    request.name = (
        f"projects/{project_id}/locations/{zone}/privateClouds/{private_cloud_name}"
        f"/clusters/{cluster_name}"
    )
    return client.delete_cluster(request)


# [END vmwareengine_delete_cluster]
