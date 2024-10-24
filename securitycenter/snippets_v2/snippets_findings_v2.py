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
from typing import Dict


# [START securitycenter_list_all_findings_v2]
def list_all_findings(organization_id, source_name, location_id) -> int:
    """
    lists all findings for a source
    Args:
       organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
       source_name: is the resource path for a source that has been created
       location_id: GCP location id; example: 'global'
    Returns:
        int: returns the count of all findings for a source
    """
    from google.cloud import securitycenter_v2

    # Create a client.
    client = securitycenter_v2.SecurityCenterClient()
    parent = f"organizations/{organization_id}"
    all_sources = f"{parent}/sources/{source_name}/locations/{location_id}"

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
    return finding_result_iterator


# [END securitycenter_list_all_findings_v2]


# [START securitycenter_list_filtered_findings_v2]
def list_filtered_findings(organization_id, source_name, location_id) -> int:
    """
    lists filtered findings for a source
    Args:
        organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
        source_name: is the resource path for a source that has been created
        location_id: GCP location id; example: 'global'
    Returns:
         int: returns the filtered findings for a source
    """
    count = 0
    from google.cloud import securitycenter_v2

    # Create a new client.
    client = securitycenter_v2.SecurityCenterClient()
    parent = f"organizations/{organization_id}"
    all_sources = f"{parent}/sources/{source_name}/locations/{location_id}"
    finding_result_iterator = client.list_findings(
        request={"parent": all_sources, "filter": 'severity="LOW"'}
    )
    # Iterate an print all finding names and the resource they are
    # in reference to.
    for count, finding_result in enumerate(finding_result_iterator):
        print(
            "{}: name: {} resource: {}".format(
                count, finding_result.finding.name, finding_result.finding.resource_name
            )
        )
    return count


# [END securitycenter_list_filtered_findings_v2]


# [START securitycenter_group_all_findings_v2]
def group_all_findings(organization_id, source_name, location_id) -> int:
    """
    Demonstrates grouping all findings across an organization.
    Args:
        organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
        source_name: is the resource path for a source that has been created
        location_id: GCP location id; example: 'global'
    Returns:
         int: returns the count of groups all findings for a source across the organization.
    """
    count = 0
    from google.cloud import securitycenter_v2

    # Create a client.
    client = securitycenter_v2.SecurityCenterClient()
    parent = f"organizations/{organization_id}"
    all_sources = f"{parent}/sources/{source_name}/locations/{location_id}"

    group_result_iterator = client.group_findings(
        request={"parent": all_sources, "group_by": "category"}
    )
    for count, group_result in enumerate(group_result_iterator):
        print((count + 1), group_result)
    return count


# [END securitycenter_group_all_findings_v2]


# [START securitycenter_group_filtered_findings_v2]
def group_filtered_findings(organization_id, source_name, location_id) -> int:
    """
    Demonstrates grouping all filtered findings across an organization.
    Args:
        organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
        source_name: is the resource path for a source that has been created
        location_id: GCP location id; example: 'global'
    Returns:
         int: returns the count of groups all filtered findings for a source across the organization.
    """
    count = 0
    from google.cloud import securitycenter_v2

    # Create a client.
    client = securitycenter_v2.SecurityCenterClient()
    parent = f"organizations/{organization_id}"
    all_sources = f"{parent}/sources/{source_name}/locations/{location_id}"

    group_result_iterator = client.group_findings(
        request={
            "parent": all_sources,
            "group_by": "category",
            "filter": 'state="ACTIVE"',
        }
    )
    for count, group_result in enumerate(group_result_iterator):
        print((count + 1), group_result)
    return count


# [END securitycenter_group_filtered_findings_v2]


# [START securitycenter_list_findings_with_security_marks_v2]
def list_findings_with_security_marks(organization_id, source_name, location_id) -> int:
    """
    lists all filtered findings with security marks across an organization.
    Args:
        organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
        source_name: is the resource path for a source that has been created
        location_id: GCP location id; example: 'global'
    Returns:
         int: returns the count of filtered findings with security marks across the organization.
    """
    count = 0
    from google.cloud import securitycenter_v2

    # Create a new client.
    client = securitycenter_v2.SecurityCenterClient()
    parent = f"organizations/{organization_id}"
    all_sources = f"{parent}/sources/{source_name}/locations/{location_id}"
    # below filter is used to list active and unmuted findings without security marks acknowledgement as true.
    finding_result_iterator = client.list_findings(
        request={
            "parent": all_sources,
            "filter": 'NOT security_marks.marks.ACK="true" AND NOT mute="MUTED" AND state="ACTIVE"',
        }
    )
    # Iterate an print all finding names and the resource they are
    # in reference to.
    for count, finding_result in enumerate(finding_result_iterator):
        print(
            "{}: name: {} resource: {}".format(
                count, finding_result.finding.name, finding_result.finding.resource_name
            )
        )
    return count


# [END securitycenter_list_findings_with_security_marks_v2]


# [START securitycenter_group_findings_by_state_v2]
def group_findings_by_state(organization_id, source_name, location_id) -> int:
    """
    groups the findings across an organization.
    Args:
        organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
        source_name: is the resource path for a source that has been created
        location_id: GCP location id; example: 'global'
    Returns:
         int: returns the count of group findings for a source across the organization.
    """
    count = 0
    from google.cloud import securitycenter_v2

    # Create a client.
    client = securitycenter_v2.SecurityCenterClient()
    parent = f"organizations/{organization_id}"
    all_sources = f"{parent}/sources/{source_name}/locations/{location_id}"

    group_result_iterator = client.group_findings(
        request={"parent": all_sources, "group_by": "state"}
    )
    for count, group_result in enumerate(group_result_iterator):
        print((count + 1), group_result)
    return count


# [END securitycenter_group_findings_by_state_v2]


# [START securitycenter_create_finding_v2]
def create_finding(
    organization_id, location_id, finding_id, source_name, category
) -> Dict:
    """
    cretaes a new finding
    Args:
        organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
        source_name: is the resource path for a source that has been created
        finding_id: unique identifier provided by the client.
        location_id: GCP location id; example: 'global'
        category: the additional category group with in findings.
    Returns:
         Dict: returns the created findings details.
    """
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
    resource_name = (
        f"//cloudresourcemanager.googleapis.com/organizations/{organization_id}"
    )

    finding = Finding(
        state=Finding.State.ACTIVE,
        resource_name=resource_name,
        category=category,
        event_time=event_time,
    )
    parent = source_name + "/locations/" + location_id
    # Call The API.
    created_finding = client.create_finding(
        request={"parent": parent, "finding_id": finding_id, "finding": finding}
    )
    print(created_finding)
    return created_finding


# [END securitycenter_create_finding_v2]


# [START securitycenter_update_finding_source_properties_v2]
def update_finding(source_name, location_id) -> Dict:
    """
    updates a finding
    Args:
        source_name: is the resource path for a source that has been created
        location_id: GCP location id; example: 'global'
    Returns:
         Dict: returns the updated findings details.
    """
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


# [START securitycenter_create_source_v2]
def create_source(organization_id) -> Dict:
    """
    Create a new findings source
    Args:
        organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
    Returns:
         Dict: returns the created findings source details.
    """
    from google.cloud import securitycenter_v2

    client = securitycenter_v2.SecurityCenterClient()
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


# [END securitycenter_create_source_v2]


# [START securitycenter_get_source_v2]
def get_source(source_name) -> Dict:
    """
    Gets the details of an existing source.
    Args:
        source_name: is the resource path for a source that has been created
    Returns:
         Dict: returns the details of existing source.
    """
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
    return source


# [END securitycenter_get_source_v2]


# [START securitycenter_update_source_v2]
def update_source(source_name) -> Dict:
    """
    Updates a source's display name.
    Args:
        source_name: is the resource path for a source that has been created
    Returns:
         Dict: returns the details of updated source.
    """
    from google.cloud import securitycenter_v2
    from google.protobuf import field_mask_pb2

    client = securitycenter_v2.SecurityCenterClient()

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
    return updated


# [END securitycenter_update_source_v2]


# [START securitycenter_list_sources_v2]
def list_source(organization_id) -> int:
    """
    lists the findings source
    Args:
        organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
    Returns:
         Dict: returns the count of the findings source
    """
    count = -1
    from google.cloud import securitycenter_v2

    # Create a new client.
    client = securitycenter_v2.SecurityCenterClient()
    # 'parent' must be in one of the following formats:
    #   "organizations/{organization_id}"
    #   "projects/{project_id}"
    #   "folders/{folder_id}"
    parent = f"organizations/{organization_id}"

    # Call the API and print out each existing source.
    for count, source in enumerate(client.list_sources(request={"parent": parent})):
        print(count, source)
    return count


# [END securitycenter_list_sources_v2]


# [START securitycenter_get_source_iam_v2]
def get_iam_policy(organization_id, source_name) -> Dict:
    """
    Gets the iam policy of the source.
    Args:
        organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
        source_name: is the resource path for a source that has been created
    Returns:
        Dict: returns the iam policy
    """
    from google.cloud import securitycenter_v2

    client = securitycenter_v2.SecurityCenterClient()
    source_name = f"organizations/{organization_id}/sources/{source_name}"
    policy = client.get_iam_policy(request={"resource": source_name})
    print(f"Policy: {policy}")
    return policy


# [END securitycenter_get_source_iam_v2]


# [START securitycenter_set_source_iam_v2]
def set_source_iam_policy(organization_id, source_name, user_email, role_id) -> Dict:
    """
    Gives a user findingsEditor permission to the source.
    Args:
        organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
        source_name: is the resource path for a source that has been created
        user_email: user_email is an e-mail address known to Cloud IAM (e.g. a gmail address).user_mail = user@somedomain.com
        role_id: role_id to assign
    Returns:
        Dict: returns the source iam policy
    """
    from google.cloud import securitycenter_v2
    from google.iam.v1 import policy_pb2

    client = securitycenter_v2.SecurityCenterClient()
    source_name = f"organizations/{organization_id}/sources/{source_name}"
    # Get the old policy so we can do an incremental update.
    old_policy = client.get_iam_policy(request={"resource": source_name})
    print(f"Old Policy: {old_policy}")

    # Setup a new IAM binding.
    binding = policy_pb2.Binding()
    binding.role = role_id
    binding.members.append(f"user:{user_email}")

    # Setting the e-tag avoids over-write existing policy
    updated = client.set_iam_policy(
        request={
            "resource": source_name,
            "policy": {"etag": old_policy.etag, "bindings": [binding]},
        }
    )

    print(f"Updated Policy: {updated}")
    return updated


# [END securitycenter_set_source_iam_v2]


# [START securitycenter_test_iam_v2]
def troubleshoot_iam_permissions(organization_id, source_name, permissions):
    """
    Demonstrate calling test_iam_permissions to determine if the
    service account has the correct permisions.
    Args:
       organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
       source_name: is the resource path for a source that has been created
       permissions:
    Returns:
       Dict: returns the source iam policy
    """
    from google.cloud import securitycenter_v2

    # Create a client.
    client = securitycenter_v2.SecurityCenterClient()
    source_name = f"organizations/{organization_id}/sources/{source_name}"
    # Check for permssions to call create_finding or update_finding.
    permission_response = client.test_iam_permissions(
        request={
            "resource": source_name,
            "permissions": permissions,
        }
    )

    print(
        "Permision to create or update findings? {}".format(
            len(permission_response.permissions) > 0
        )
    )
    return permission_response


# [END securitycenter_test_iam_v2]
