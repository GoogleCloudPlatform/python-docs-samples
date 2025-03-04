#  Copyright 2016 Google, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from google.cloud.dns import ManagedZone
from google.cloud.exceptions import NotFound


def get_zone(project_id: str, zone_name: str) -> ManagedZone | None:
    """Gets a Cloud DNS managedZone.

    Find more information about the ManagedZone object at:
    https://cloud.google.com/dns/docs/reference/rest/v1/managedZones#ManagedZone

    Args:
        project_id: The project ID to use.
        name: The name of the zone to get.

    Returns:
        The zone object if found, otherwise None.

    Raises:
        NotFound: If the zone is not found.
    """

    # [START dns_get_zone]
    from google.cloud.dns import Client

    # TODO(developer): Update and uncomment the following lines:
    # project_id = "my_project_id"
    # zone_name = "my_zone_name"

    client = Client(project_id)
    zone = client.zone(zone_name)
    # [END dns_get_zone]

    try:
        zone.reload()
        return zone
    except NotFound:
        return None
