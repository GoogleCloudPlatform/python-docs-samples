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
  # [START securitycenter_list_all_findings]
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
  # [END securitycenter_list_all_findings]
  return count


def list_filtered_findings(organization_id, source_id, location_id):
  count = 0
  # [START securitycenter_list_filtered_findings]
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
  # [END securitycenter_list_filtered_findings]
  return count


def group_all_findings(organization_id, source_id, location_id):
  """Demonstrates grouping all findings across an organization."""
  count = 0
  # [START securitycenter_group_all_findings]
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
  # [END securitycenter_group_all_findings]
  return count


def group_filtered_findings(organization_id, source_id, location_id):
  """Demonstrates grouping all findings across an organization."""
  count = 0
  # [START securitycenter_group_filtered_findings]
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
  # [END securitycenter_group_filtered_findings]
  return count

