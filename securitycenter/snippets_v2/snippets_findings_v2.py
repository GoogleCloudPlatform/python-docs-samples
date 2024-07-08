#!/usr/bin/env python
#
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Examples of working with source and findings in Security Command Center."""

def list_all_findings(organization_id, location_id):
  i = 0
  # [START securitycenter_list_all_findings]
  from google.cloud import securitycenter_v2

  # Create a client.
  client = securitycenter_v2.SecurityCenterClient()

  # 'parent' must be in one of the following formats:
  #   "organizations/{organization_id}"
  #   "projects/{project_id}"
  #   "folders/{folder_id}"
  parent = f"organizations/{organization_id}"
  # The "sources/-" suffix lists findings across all sources.  You
  # also use a specific source_name instead.
  all_sources = f"{parent}/sources/-/locations/{location_id}"
  # Create the request dictionary
  request = {"parent": all_sources}

  # Print the request for debugging
  print("Request: ", request)

  finding_result_iterator = client.list_findings(request={"parent": all_sources})
  for i, finding_result in enumerate(finding_result_iterator):
    print(
        "{}: name: {} resource: {}".format(
            i, finding_result.finding.name, finding_result.finding.resource_name
        )
    )
  # [END securitycenter_list_all_findings]
  return i


def list_filtered_findings(source_name):
  i = 0
  # [START securitycenter_list_filtered_findings]
  from google.cloud import securitycenter_v2

  # Create a new client.
  client = securitycenter_v2.SecurityCenterClient()

  # 'source_name' is the resource path for a source that has been
  # created previously (you can use list_sources to find a specific one).
  # Its format is:
  # source_name = f"{parent}/sources/{source_id}"
  # 'parent' must be in one of the following formats:
  #   "organizations/{organization_id}"
  #   "projects/{project_id}"
  #   "folders/{folder_id}"
  # You an also use a wild-card "-" for all sources:
  #   source_name = "organizations/111122222444/sources/-/locations/{location_id}"
  finding_result_iterator = client.list_findings(
      request={"parent": source_name, "filter": 'severity="MEDIUM"'}
  )
  # Iterate an print all finding names and the resource they are
  # in reference to.
  for i, finding_result in enumerate(finding_result_iterator):
    print(
        "{}: name: {} resource: {}".format(
            i, finding_result.finding.name, finding_result.finding.resource_name
        )
    )
  # [END securitycenter_list_filtered_findings]
  return i


def group_all_findings(organization_id, location_id):
  """Demonstrates grouping all findings across an organization."""
  i = 0
  # [START securitycenter_group_all_findings]
  from google.cloud import securitycenter_v2

  # Create a client.
  client = securitycenter_v2.SecurityCenterClient()

  # 'parent' must be in one of the following formats:
  #   "organizations/{organization_id}"
  #   "projects/{project_id}"
  #   "folders/{folder_id}"
  parent = f"organizations/{organization_id}"
  # The "sources/-" suffix lists findings across all sources.  You
  # also use a specific source_name instead.
  all_sources = f"{parent}/sources/-/locations/{location_id}"
  group_result_iterator = client.group_findings(
      request={"parent": all_sources, "group_by": "category"}
  )
  for i, group_result in enumerate(group_result_iterator):
    print((i + 1), group_result)
  # [END securitycenter_group_all_findings]
  return i


def group_filtered_findings(source_name):
  """Demonstrates grouping all findings across an organization."""
  i = 0
  # [START securitycenter_group_filtered_findings]
  from google.cloud import securitycenter_v2

  # Create a client.
  client = securitycenter_v2.SecurityCenterClient()

  # 'source_name' is the resource path for a source that has been
  # created previously (you can use list_sources to find a specific one).
  # Its format is:
  # source_name = "{parent}/sources/{source_id}"
  # 'parent' must be in one of the following formats:
  #   "organizations/{organization_id}"
  #   "projects/{project_id}"
  #   "folders/{folder_id}"
  # source_name = "organizations/111122222444/sources/1234/locations/{location_id}"

  group_result_iterator = client.group_findings(
      request={
          "parent": source_name,
          "group_by": "category",
          "filter": 'state="ACTIVE"',
      }
  )
  for i, group_result in enumerate(group_result_iterator):
    print((i + 1), group_result)
  # [END securitycenter_group_filtered_findings]
  return i


def create_source(organization_id):
  """Create a new findings source."""
  # [START securitycenter_create_source]
  from google.cloud import securitycenter_v2

  client = securitycenter_v2.SecurityCenterClient()
  # organization_id is the numeric ID of the organization. e.g.:
  # organization_id = "111122222444"
  org_name = f"organizations/{organization_id}"

  created = client.create_source(
      request={
          "parent": org_name,
          "source": {
              "display_name": "Customized Display Name",
              "description": "A new custom source that does X",
          },
      }
  )
  print(f"Created Source: {created.name}")
  # [END securitycenter_create_source]


def get_source(source_name):
  """Gets an existing source."""
  # [START securitycenter_get_source]
  from google.cloud import securitycenter_v2

  client = securitycenter_v2.SecurityCenterClient()

  # 'source_name' is the resource path for a source that has been
  # created previously (you can use list_sources to find a specific one).
  # Its format is:
  # source_name = "organizations/{organization_id}/sources/{source_id}"
  # e.g.:
  # source_name = "organizations/111122222444/sources/1234"
  source = client.get_source(request={"name": source_name})

  print(f"Source: {source}")
  # [END securitycenter_get_source]
  return source


def update_source(source_name):
  """Updates a source's display name."""
  # [START securitycenter_update_source]
  from google.cloud import securitycenter
  from google.protobuf import field_mask_pb2

  client = securitycenter.SecurityCenterClient()

  # Field mask to only update the display name.
  field_mask = field_mask_pb2.FieldMask(paths=["display_name"])

  # 'source_name' is the resource path for a source that has been
  # created previously (you can use list_sources to find a specific one).
  # Its format is:
  # source_name = "organizations/{organization_id}/sources/{source_id}"
  # e.g.:
  # source_name = "organizations/111122222444/sources/1234"
  updated = client.update_source(
      request={
          "source": {"name": source_name, "display_name": "Updated Display Name"},
          "update_mask": field_mask,
      }
  )
  print(f"Updated Source: {updated}")
  # [END securitycenter_update_source]
  return updated


def list_source(organization_id):
  """Lists finding sources."""
  i = -1
  # [START securitycenter_list_sources]
  from google.cloud import securitycenter

  # Create a new client.
  client = securitycenter.SecurityCenterClient()
  # 'parent' must be in one of the following formats:
  #   "organizations/{organization_id}"
  #   "projects/{project_id}"
  #   "folders/{folder_id}"
  parent = f"organizations/{organization_id}"

  # Call the API and print out each existing source.
  for i, source in enumerate(client.list_sources(request={"parent": parent})):
    print(i, source)
  # [END securitycenter_list_sources]
  return i
