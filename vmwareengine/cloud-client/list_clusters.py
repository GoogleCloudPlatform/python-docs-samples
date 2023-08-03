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

# [START vmwareengine_list_clusters]
from typing import Iterable

from google.cloud import vmwareengine_v1


def list_clusters(
    project_id: str, zone: str, private_cloud_name: str
) -> Iterable[vmwareengine_v1.Cluster]:
    """
    Retrieves a list of clusters in private cloud.

    Args:
        project_id: name of the project hosting the private cloud.
        zone: zone in which the private cloud is located.
        private_cloud_name: name of the cloud of which you want to list cluster.

    Returns:
        An iterable collection of Cluster objects.
    """
    client = vmwareengine_v1.VmwareEngineClient()
    return client.list_clusters(
        parent=f"projects/{project_id}/locations/{zone}/privateClouds/{private_cloud_name}"
    )


# [END vmwareengine_list_clusters]
