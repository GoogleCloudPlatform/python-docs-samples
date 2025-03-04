# Copyright 2025 Google LLC
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

from google.cloud.dns import ManagedZone


def create_zone(project_id: str, zone_name: str, dns_name: str, description: str) -> ManagedZone:
    """Creates a Cloud DNS ManagedZone.

    Args:
        project_id: The project ID to use.
        name: The name of the zone to create. Must be unique within the project.
        dns_name: The DNS name of the zone.
        description: A description of the zone.

    Returns:
        The created zone object.
    """

    # [START dns_create_zone]
    from google.cloud.dns import Client

    # TODO(developer): Uncomment the following lines:
    # project_id = "my_project_id"
    # zone_name = "my_zone_name"
    # dns_name = "example.com."
    # description = "Description for your ManagedZone."

    client = Client(project_id)

    # Find more information about the ManagedZone object at:
    # https://cloud.google.com/dns/docs/reference/rest/v1/managedZones#ManagedZone
    zone = client.zone(
        zone_name,
        dns_name,
        description,
    )
    zone.create()
    # [END dns_create_zone]

    return zone
