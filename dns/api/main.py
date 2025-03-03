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

from __future__ import annotations

from google.cloud.dns import Client, ManagedZone
from google.cloud.exceptions import NotFound


# [START dns_create_zone]
def create_zone(project_id: str, name: str, dns_name: str, description: str) -> ManagedZone:
    """Creates a Cloud DNS ManagedZone.

    Find more information about the ManagedZone object at:
    https://cloud.google.com/dns/docs/reference/rest/v1/managedZones#ManagedZone

    Args:
        project_id: The project ID to use.
        name: The name of the zone to create. Must be unique within the project.
        dns_name: The DNS name of the zone.
        description: A description of the zone.

    Returns:
        The created zone object.
    """

    client = Client(project=project_id)
    zone = client.zone(
        name,  # example_zone_name
        dns_name=dns_name,  # example.com.
        description=description,
    )
    zone.create()
    return zone
# [END dns_create_zone]


# [START dns_get_zone]
def get_zone(project_id: str, name: str) -> ManagedZone | None:
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

    client = Client(project=project_id)
    zone = client.zone(name=name)

    try:
        zone.reload()
        return zone
    except NotFound:
        return None
# [END dns_get_zone]


# [START dns_list_zones]
def list_zones(project_id: str) -> list[str]:
    """Gets a list of all Cloud DNS zones in the specified project.

    Args:
        project_id: The project ID to use.

    Returns:
        A list of zone names.
    """

    client = Client(project=project_id)
    zones = client.list_zones()
    return [zone.name for zone in zones]
# [END dns_list_zones]


# [START dns_delete_zone]
def delete_zone(project_id: str, name: str) -> None:
    """Deletes a Cloud DNS zone.

    Args:
        project_id: The project ID to use.
        name: The name of the zone to delete.

    Raises:
        NotFound: If the zone is not found.
    """
    client = Client(project=project_id)
    zone = client.zone(name)
    zone.delete()
# [END dns_delete_zone]


# [START dns_list_resource_records]
def list_resource_records(project_id: str, zone_name: str) -> list[tuple[str, str, int, list[str]]]:
    """Lists the resource record sets for a zone.

    Find more information about the ResourceRecordSet object at:
    https://cloud.google.com/dns/docs/reference/rest/v1/resourceRecordSets#resource:-resourcerecordset

    Args:
        project_id: The project ID to use.
        zone_name: The name of the zone to list resource records for.

    Returns:
        A list of tuples, where each tuple contains:
        - The record name (str).
        - The record type (str).
        - The record TTL (int).
        - The record data (list of str).
    """
    client = Client(project=project_id)
    zone = client.zone(zone_name)

    records = zone.list_resource_record_sets()

    return [
        (record.name, record.record_type, record.ttl, record.rrdatas)
        for record in records
    ]
# [END dns_list_resource_records]


# [START dns_list_changes]
def list_changes(project_id: str, zone_name: str) -> list[tuple[str, str]]:
    """Lists the changes for a zone.

    Find more information about the Change object at:
    https://cloud.google.com/dns/docs/reference/rest/v1/changes#resource:-change

    Args:
        project_id: The project ID to use.
        zone_name: The name of the zone to list changes for.

    Returns:
        A list of tuples, where each tuple contains:
        - The change start time (str).
        - The change status (str).
    """
    client = Client(project=project_id)
    zone = client.zone(zone_name)

    changes = zone.list_changes()

    return [(change.started, change.status) for change in changes]
# [END dns_list_changes]
