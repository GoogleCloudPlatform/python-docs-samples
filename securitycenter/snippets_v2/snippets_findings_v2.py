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

def list_all_findings(organization_id, source_id, location_id):
  count = 0
  # [START securitycenter_list_all_findings_v2]
  from google.cloud import securitycenter_v2

  # Create a client.
  client = securitycenter_v2.SecurityCenterClient()

  # 'parent' must be in one of the following formats:
  #   "organizations/{organization_id}"
  #   "projects/{project_id}"
  #   "folders/{folder_id}"
  parent = f"organizations/{organization_id}"

  # 'source_id' to scope the findings.
  # The "sources/-" suffix lists findings across all sources.  You
  # also use a specific source_name instead.
  # location_id= "global"
  all_sources = f"{parent}/sources/{source_id}/locations/{location_id}"

  # Create the request dictionary
  request = {"parent": all_sources}

  # Print the request for debugging
  print("Request: ", request)

  finding_result_iterator = client.list_findings(request={"parent": all_sources})
  for count, finding_result in enumerate(finding_result_iterator):
    print(
        "{}: name: {} resource: {}".format(
            count, finding_result.finding.name, finding_result.finding.resource_name
        )
    )
  # [END securitycenter_list_all_findings_v2]
  return count


def list_filtered_findings(organization_id, source_id, location_id):
  count = 0
  # [START securitycenter_list_filtered_findings_v2]
  from google.cloud import securitycenter_v2

  # Create a new client.
  client = securitycenter_v2.SecurityCenterClient()

  # 'parent' must be in one of the following formats:
  #   "organizations/{organization_id}"
  #   "projects/{project_id}"
  #   "folders/{folder_id}"
  parent = f"organizations/{organization_id}"

  # 'source_id' to scope the findings.
  # The "sources/-" suffix lists findings across all sources.  You
  # also use a specific source_name instead.
  # location_id= "global"
  all_sources = f"{parent}/sources/{source_id}/locations/{location_id}"
  finding_result_iterator = client.list_findings(
      request={"parent": all_sources, "filter": 'severity="MEDIUM"'}
  )
  # Iterate an print all finding names and the resource they are
  # in reference to.
  for count, finding_result in enumerate(finding_result_iterator):
    print(
        "{}: name: {} resource: {}".format(
            count, finding_result.finding.name, finding_result.finding.resource_name
        )
    )
  # [END securitycenter_list_filtered_findings_v2]
  return count


def group_all_findings(organization_id, source_id, location_id):
  """Demonstrates grouping all findings across an organization."""
  count = 0
  # [START securitycenter_group_all_findings_v2]
  from google.cloud import securitycenter_v2

  # Create a client.
  client = securitycenter_v2.SecurityCenterClient()

  # 'parent' must be in one of the following formats:
  #   "organizations/{organization_id}"
  #   "projects/{project_id}"
  #   "folders/{folder_id}"
  parent = f"organizations/{organization_id}"

  # 'source_id' to scope the findings.
  # The "sources/-" suffix lists findings across all sources.  You
  # also use a specific source_name instead.
  # location_id= "global"
  all_sources = f"{parent}/sources/{source_id}/locations/{location_id}"

  group_result_iterator = client.group_findings(
      request={"parent": all_sources, "group_by": "category"}
  )
  for count, group_result in enumerate(group_result_iterator):
    print((count + 1), group_result)
  # [END securitycenter_group_all_findings_v2]
  return count


def group_filtered_findings(organization_id, source_id, location_id):
  """Demonstrates grouping all findings across an organization."""
  count = 0
  # [START securitycenter_group_filtered_findings_v2]
  from google.cloud import securitycenter_v2

  # Create a client.
  client = securitycenter_v2.SecurityCenterClient()

  # 'parent' must be in one of the following formats:
  #   "organizations/{organization_id}"
  #   "projects/{project_id}"
  #   "folders/{folder_id}"
  parent = f"organizations/{organization_id}"

  # 'source_id' to scope the findings.
  # The "sources/-" suffix lists findings across all sources.  You
  # also use a specific source_name instead.
  # location_id= "global"
  all_sources = f"{parent}/sources/{source_id}/locations/{location_id}"

  group_result_iterator = client.group_findings(
      request={
          "parent": all_sources,
          "group_by": "category",
          "filter": 'state="ACTIVE"',
      }
  )
  for count, group_result in enumerate(group_result_iterator):
    print((count + 1), group_result)
  # [END securitycenter_group_filtered_findings_v2]
  return count


def list_findings_with_security_marks(organization_id, source_id, location_id):
  count = 0
  # [START securitycenter_list_findings_with_security_marks_v2]
  from google.cloud import securitycenter_v2

  # Create a new client.
  client = securitycenter_v2.SecurityCenterClient()

  # 'parent' must be in one of the following formats:
  #   "organizations/{organization_id}"
  #   "projects/{project_id}"
  #   "folders/{folder_id}"
  parent = f"organizations/{organization_id}"

  # 'source_id' to scope the findings.
  # The "sources/-" suffix lists findings across all sources.  You
  # also use a specific source_name instead.
  # location_id= "global"
  all_sources = f"{parent}/sources/{source_id}/locations/{location_id}"
  finding_result_iterator = client.list_findings(
      request={"parent": all_sources, "filter": 'NOT security_marks.marks.ACK="true" AND NOT mute="MUTED" AND state="ACTIVE"'}
  )
  # Iterate an print all finding names and the resource they are
  # in reference to.
  for count, finding_result in enumerate(finding_result_iterator):
    print(
        "{}: name: {} resource: {}".format(
            count, finding_result.finding.name, finding_result.finding.resource_name
        )
    )
  # [END securitycenter_list_findings_with_security_marks_v2]
  return count


def group_findings_by_state(organization_id, source_id, location_id):
  """Demonstrates grouping all findings across an organization."""
  count = 0
  # [START securitycenter_group_findings_by_state_v2]
  from google.cloud import securitycenter_v2

  # Create a client.
  client = securitycenter_v2.SecurityCenterClient()

  # 'parent' must be in one of the following formats:
  #   "organizations/{organization_id}"
  #   "projects/{project_id}"
  #   "folders/{folder_id}"
  parent = f"organizations/{organization_id}"

  # 'source_id' to scope the findings.
  # The "sources/-" suffix lists findings across all sources.  You
  # also use a specific source_name instead.
  # location_id= "global"
  all_sources = f"{parent}/sources/{source_id}/locations/{location_id}"

  group_result_iterator = client.group_findings(
      request={"parent": all_sources, "group_by": "state"}
  )
  for count, group_result in enumerate(group_result_iterator):
    print((count + 1), group_result)
  # [END securitycenter_group_findings_by_state_v2]
  return count


def create_source(organization_id):
  """Create a new findings source."""
  # [START securitycenter_create_source]
  from google.cloud import securitycenter_v2

  client = securitycenter_v2.SecurityCenterClient()
  # organization_id is the numeric ID of the organization. e.g.:
  # organization_id = "111122222444"
  org_name = f"organizations/{organization_id}"

  response = client.create_source(
      request={
          "parent": org_name,
          "source": {
              "display_name": "Customized Display Name",
              "description": "A new custom source that does X",
          },
      }
  )
  print(f"Created Source: {response.name}")
  return response
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
  count = -1
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
  for count, source in enumerate(client.list_sources(request={"parent": parent})):
    print(count, source)
  # [END securitycenter_list_sources]
  return count

def create_finding(organization_id, location_id, finding_id, source_name, category):
  """Creates a new finding."""
  # [START securitycenter_create_finding_v2]
  import datetime

  from google.cloud import securitycenter_v2
  from google.cloud.securitycenter_v2 import Finding

  # Create a new client.
  client = securitycenter_v2.SecurityCenterClient()

  # Use the current time as the finding "event time".
  event_time = datetime.datetime.now(tz=datetime.timezone.utc)

  # 'source_name' is the resource path for a source that has been
  # created previously (you can use list_sources to find a specific one).
  # Its format is:
  # source_name = "organizations/{organization_id}/sources/{source_id}"
  # e.g.:
  # source_name = "organizations/111122222444/sources/1234"
  # source_name = f"organizations/{organization_id}/sources/{source_name}"
  # category= "MEDIUM_RISK_ONE"
  # The resource this finding applies to.  The CSCC UI can link
  # the findings for a resource to the corresponding Asset of a resource
  # if there are matches.
  resource_name = f"//cloudresourcemanager.googleapis.com/organizations/{organization_id}"

  finding = Finding(
      state=Finding.State.ACTIVE,
      resource_name=resource_name,
      category=category,
      event_time=event_time,
  )
  parent = source_name+"/locations/"+location_id
  # Call The API.
  created_finding = client.create_finding(
      request={"parent": parent, "finding_id": finding_id, "finding": finding}
  )
  print(created_finding)
  # [END securitycenter_create_finding_v2]
  return created_finding


def update_finding(source_name, location_id):
  # [START securitycenter_update_finding_source_properties_v2]
  import datetime

  from google.cloud import securitycenter_v2
  from google.cloud.securitycenter_v2 import Finding
  from google.protobuf import field_mask_pb2

  client = securitycenter_v2.SecurityCenterClient()
  # Only update the specific source property and event_time.  event_time
  # is required for updates.
  field_mask = field_mask_pb2.FieldMask(
      paths=["source_properties.s_value", "event_time"]
  )

  # Set the update time to Now.  This must be some time greater then the
  # event_time on the original finding.
  event_time = datetime.datetime.now(tz=datetime.timezone.utc)

  # 'source_name' is the resource path for a source that has been
  # created previously (you can use list_sources to find a specific one).
  # Its format is:
  # source_name = "organizations/{organization_id}/sources/{source_id}"
  # e.g.:
  # source_name = "organizations/111122222444/sources/1234"
  finding_name = f"{source_name}/locations/{location_id}/findings/samplefindingid"
  finding = Finding(
      name=finding_name,
      source_properties={"s_value": "new_string"},
      event_time=event_time,
  )
  updated_finding = client.update_finding(
      request={"finding": finding, "update_mask": field_mask}
  )

  print(
      "New Source properties: {}, Event Time {}".format(
          updated_finding.source_properties, updated_finding.event_time
      )
  )
  return updated_finding
  # [END securitycenter_update_finding_source_properties_v2]

