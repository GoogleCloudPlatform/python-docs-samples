# Copyright 2016 Google, Inc.
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

def list_zones(project_id: str) -> list[str]:
    """Gets a list of all Cloud DNS zones in the specified project.

    Args:
        project_id: The project ID to use.

    Returns:
        A list of zone names.
    """

    # [START dns_list_zones]
    from google.cloud.dns import Client

    # TODO(developer): Update and uncomment the following lines:
    # project_id = "my_project_id"

    client = Client(project_id)
    zones = client.list_zones()
    # [END dns_list_zones]

    return [zone.name for zone in zones]
