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

from google.cloud import vmwareengine_v1


def create_private_cloud(project_id: str, zone: str, network_name: str, cloud_name: str, cluster_name: str) -> vmwareengine_v1.PrivateCloud():
    client = vmwareengine_v1.VmwareEngineClient()

    request = vmwareengine_v1.CreatePrivateCloudRequest()
    request.parent = f"projects/{project_id}/locations/{zone}"
    request.private_cloud_id = cloud_name

    request.private_cloud = vmwareengine_v1.PrivateCloud()
    request.private_cloud.management_cluster = vmwareengine_v1.PrivateCloud.ManagementCluster()
    request.private_cloud.management_cluster.cluster_id = cluster_name
    node_config = vmwareengine_v1.NodeTypeConfig()
    node_config.node_count = 3
    request.private_cloud.management_cluster.node_type_configs = {
        "standard-72": node_config
    }

    request.private_cloud.network_config = vmwareengine_v1.NetworkConfig()
    request.private_cloud.network_config.vmware_engine_network = network_name
    request.private_cloud.network_config.management_cidr = "192.168.0.0/24"

    return client.create_private_cloud(request).result(timeout=3600)

