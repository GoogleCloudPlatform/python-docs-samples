# Copyright 2016 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations


def list_zones(project_id: str) -> list[str]:
    """Gets a list of all Cloud DNS zones in the specified project.

    Args:
        project_id: The project ID to use.

    Returns:
        A list of zone names.
    """

    # [START dns_list_zones]
    from google.cloud.dns import Client

    client = Client(project=project_id)
    zones = client.list_zones()
    # [END dns_list_zones]

    return [zone.name for zone in zones]


def delete_zone(project_id: str, zone_name: str) -> None:
    """Deletes a Cloud DNS zone.

    Args:
        project_id: The project ID to use.
        zone_name: The name of the zone to delete.

    Raises:
        NotFound: If the zone is not found.
    """

    # [START dns_delete_zone]
    from google.cloud.dns import Client

    # TODO(developer): Update and uncomment the following lines:
    # project_id = "my_project_id"
    # zone_name = "my_zone_name"

    client = Client(project=project_id)
    zone = client.zone(zone_name)
    zone.delete()
    # [END dns_delete_zone]


def list_resource_records(project_id: str, zone_name: str) -> list[tuple[str, str, int, list[str]]]:
    """Lists the resource record sets for a zone.

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

    # [START dns_list_resource_records]
    from google.cloud.dns import Client

    # TODO(developer): Update and uncomment the following lines:
    # project_id = "my_project_id"
    # zone_name = "my_zone_name"

    client = Client(project=project_id)
    zone = client.zone(zone_name)

    # Find more information about the ResourceRecordSet object at:
    # https://cloud.google.com/dns/docs/reference/rest/v1/resourceRecordSets#resource:-resourcerecordset
    records = zone.list_resource_record_sets()
    # [END dns_list_resource_records]

    return [
        (record.name, record.record_type, record.ttl, record.rrdatas)
        for record in records
    ]


def list_changes(project_id: str, zone_name: str) -> list[tuple[str, str]]:
    """Lists the changes for a zone.

    Args:
        project_id: The project ID to use.
        zone_name: The name of the zone to list changes for.

    Returns:
        A list of tuples, where each tuple contains:
        - The change start time (str).
        - The change status (str).
    """
    # [START dns_list_changes]
    from google.cloud.dns import Client

    # TODO(developer): Uncomment the following lines:
    # project_id = "my_project_id"
    # zone_name = "my_zone_name"

    client = Client(project=project_id)
    zone = client.zone(zone_name)

    # Find more information about the Change object at:
    # https://cloud.google.com/dns/docs/reference/rest/v1/changes#resource:-change
    changes = zone.list_changes()
    # [END dns_list_changes]

    return [(change.started, change.status) for change in changes]
