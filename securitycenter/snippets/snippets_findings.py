#!/usr/bin/env python
#
# Copyright 2019 Google LLC
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

"""Examples of working with source and findings in Cloud Security Command Center."""


def create_source(organization_id):
    """Create a new findings source. """
    # [START securitycenter_create_source]
    # [START create_source]
    from google.cloud import securitycenter

    client = securitycenter.SecurityCenterClient()
    # organization_id is the numeric ID of the organization. e.g.:
    # organization_id = "111122222444"
    org_name = "organizations/{org_id}".format(org_id=organization_id)

    created = client.create_source(
        request={
            "parent": org_name,
            "source": {
                "display_name": "Customized Display Name",
                "description": "A new custom source that does X",
            },
        }
    )
    print("Created Source: {}".format(created.name))
    # [END create_source]
    # [END securitycenter_create_source]


def get_source(source_name):
    """Gets an existing source."""
    # [START securitycenter_get_source]
    # [START get_source]
    from google.cloud import securitycenter

    client = securitycenter.SecurityCenterClient()

    # source_name is the resource path for a source that has been
    # created previously (you can use list_sources to find a specific one).
    # Its format is:
    # source_name = "organizations/{organization_id}/sources/{source_id}"
    # e.g.:
    # source_name = "organizations/111122222444/sources/1234"
    source = client.get_source(request={"name": source_name})

    print("Source: {}".format(source))
    # [END get_source]
    # [END securitycenter_get_source]
    return source


def update_source(source_name):
    """Updates a source's display name."""
    # [START securitycenter_update_source]
    # [START update_source]
    from google.cloud import securitycenter
    from google.protobuf import field_mask_pb2

    client = securitycenter.SecurityCenterClient()

    # Field mask to only update the display name.
    field_mask = field_mask_pb2.FieldMask(paths=["display_name"])

    # source_name is the resource path for a source that has been
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
    print("Updated Source: {}".format(updated))
    # [END update_source]
    # [END securitycenter_update_source]
    return updated


def add_user_to_source(source_name):
    """Gives a user findingsEditor permission to the source."""
    user_email = "csccclienttest@gmail.com"
    # [START securitycenter_set_source_iam]
    # [START update_source_iam]
    from google.cloud import securitycenter
    from google.iam.v1 import policy_pb2

    client = securitycenter.SecurityCenterClient()

    # source_name is the resource path for a source that has been
    # created previously (you can use list_sources to find a specific one).
    # Its format is:
    # source_name = "organizations/{organization_id}/sources/{source_id}"
    # e.g.:
    # source_name = "organizations/111122222444/sources/1234"
    # Get the old policy so we can do an incremental update.
    old_policy = client.get_iam_policy(request={"resource": source_name})
    print("Old Policy: {}".format(old_policy))

    # Setup a new IAM binding.
    binding = policy_pb2.Binding()
    binding.role = "roles/securitycenter.findingsEditor"
    # user_email is an e-mail address known to Cloud IAM (e.g. a gmail address).
    # user_mail = user@somedomain.com
    binding.members.append("user:{}".format(user_email))

    # Setting the e-tag avoids over-write existing policy
    updated = client.set_iam_policy(
        request={
            "resource": source_name,
            "policy": {"etag": old_policy.etag, "bindings": [binding]},
        }
    )

    print("Updated Policy: {}".format(updated))

    # [END update_source_iam]
    # [END securitycenter_set_source_iam]
    return binding, updated


def list_source(organization_id):
    """Lists finding sources."""
    i = -1
    # [START securitycenter_list_sources]
    # [START list_sources]
    from google.cloud import securitycenter

    # Create a new client.
    client = securitycenter.SecurityCenterClient()
    # organization_id is the numeric ID of the organization. e.g.:
    # organization_id = "111122222444"
    org_name = "organizations/{org_id}".format(org_id=organization_id)

    # Call the API and print out each existing source.
    for i, source in enumerate(client.list_sources(request={"parent": org_name})):
        print(i, source)
    # [END list_sources]
    # [END securitycenter_list_sources]
    return i


def create_finding(source_name):
    """Creates a new finding."""
    # [START securitycenter_create_finding]
    # [START create_finding]
    from google.cloud import securitycenter
    from google.cloud.securitycenter_v1 import CreateFindingRequest, Finding
    import datetime

    # Create a new client.
    client = securitycenter.SecurityCenterClient()

    # Use the current time as the finding "event time".
    event_time = datetime.datetime.now()

    # source_name is the resource path for a source that has been
    # created previously (you can use list_sources to find a specific one).
    # Its format is:
    # source_name = "organizations/{organization_id}/sources/{source_id}"
    # e.g.:
    # source_name = "organizations/111122222444/sources/1234"

    # Controlled by caller.
    finding_id = "samplefindingid"

    # The resource this finding applies to.  The CSCC UI can link
    # the findings for a resource to the corresponding Asset of a resource
    # if there are matches.
    resource_name = "//cloudresourcemanager.googleapis.com/organizations/11232"

    finding = Finding(
        state=Finding.State.ACTIVE,
        resource_name=resource_name,
        category="MEDIUM_RISK_ONE",
        event_time=event_time,
    )

    request = CreateFindingRequest(
        parent=source_name,
        finding_id=finding_id,
        finding=finding,
    )
    # Call The API.
    created_finding = client.create_finding(
        request=request
    )
    print(created_finding)
    # [END create_finding]
    # [END securitycenter_create_finding]
    return created_finding


def create_finding_with_source_properties(source_name):
    """Demonstrate creating a new finding with source properties. """
    # [START securitycenter_create_finding_with_source_properties]
    # [START create_finding_with_properties]
    import datetime

    from google.cloud import securitycenter
    from google.cloud.securitycenter_v1 import Finding
    from google.protobuf.struct_pb2 import Value

    # Create a new client.
    client = securitycenter.SecurityCenterClient()

    # source_name is the resource path for a source that has been
    # created previously (you can use list_sources to find a specific one).
    # Its format is:
    # source_name = "organizations/{organization_id}/sources/{source_id}"
    # e.g.:
    # source_name = "organizations/111122222444/sources/1234"

    # Controlled by caller.
    finding_id = "samplefindingid2"

    # The resource this finding applies to.  The CSCC UI can link
    # the findings for a resource to the corresponding Asset of a resource
    # if there are matches.
    resource_name = "//cloudresourcemanager.googleapis.com/organizations/11232"

    # Define source properties values as protobuf "Value" objects.
    str_value = Value()
    str_value.string_value = "string_example"
    num_value = Value()
    num_value.number_value = 1234

    # Use the current time as the finding "event time".
    event_time = datetime.datetime.now()

    finding = Finding(
        state=Finding.State.ACTIVE,
        resource_name=resource_name,
        category="MEDIUM_RISK_ONE",
        source_properties={"s_value": "string_example", "n_value": 1234},
        event_time=event_time,
    )

    created_finding = client.create_finding(
        request={
            "parent": source_name,
            "finding_id": finding_id,
            "finding": finding
        }
    )
    print(created_finding)
    # [END create_finding_with_properties]
    # [END securitycenter_create_finding_with_source_properties]


def update_finding(source_name):
    # [START securitycenter_update_finding_source_properties]
    # [START update_finding]
    import datetime

    from google.cloud import securitycenter
    from google.cloud.securitycenter_v1 import Finding
    from google.protobuf import field_mask_pb2

    client = securitycenter.SecurityCenterClient()
    # Only update the specific source property and event_time.  event_time
    # is required for updates.
    field_mask = field_mask_pb2.FieldMask(
        paths=["source_properties.s_value", "event_time"]
    )

    # Set the update time to Now.  This must be some time greater then the
    # event_time on the original finding.
    event_time = datetime.datetime.now()

    # source_name is the resource path for a source that has been
    # created previously (you can use list_sources to find a specific one).
    # Its format is:
    # source_name = "organizations/{organization_id}/sources/{source_id}"
    # e.g.:
    # source_name = "organizations/111122222444/sources/1234"
    finding_name = "{}/findings/samplefindingid2".format(source_name)
    finding = Finding(
        name=finding_name,
        source_properties={"s_value": "new_string"},
        event_time=event_time,
    )
    updated_finding = client.update_finding(
        request={
            "finding": finding,
            "update_mask": field_mask,
        }
    )

    print(
        "New Source properties: {}, Event Time {}".format(
            updated_finding.source_properties, updated_finding.event_time
        )
    )
    # [END update_finding]
    # [END securitycenter_update_finding_source_properties]


def update_finding_state(source_name):
    """Demonstrate updating only a finding state."""
    # [START securitycenter_update_finding_state]
    # [START update_finding_state]
    import datetime

    from google.cloud import securitycenter
    from google.cloud.securitycenter_v1 import Finding
    # Create a client.
    client = securitycenter.SecurityCenterClient()
    # source_name is the resource path for a source that has been
    # created previously (you can use list_sources to find a specific one).
    # Its format is:
    # source_name = "organizations/{organization_id}/sources/{source_id}"
    # e.g.:
    # source_name = "organizations/111122222444/sources/1234"
    finding_name = "{}/findings/samplefindingid2".format(source_name)

    # Call the API to change the finding state to inactive as of now.
    new_finding = client.set_finding_state(
        request={
            "name": finding_name,
            "state": Finding.State.INACTIVE,
            "start_time": datetime.datetime.now(),
        }
    )
    print(f"New state: {new_finding.state}")
    # [END update_finding_state]
    # [END securitycenter_update_finding_state]


def trouble_shoot(source_name):
    """Demonstrate calling test_iam_permissions to determine if the
    service account has the correct permisions."""
    # [START securitycenter_test_iam]
    # [START test_iam_permissions]
    from google.cloud import securitycenter

    # Create a client.
    client = securitycenter.SecurityCenterClient()
    # source_name is the resource path for a source that has been
    # created previously (you can use list_sources to find a specific one).
    # Its format is:
    # source_name = "organizations/{organization_id}/sources/{source_id}"
    # e.g.:
    # source_name = "organizations/111122222444/sources/1234"

    # Check for permssions to call create_finding or update_finding.
    permission_response = client.test_iam_permissions(
        request={
            "resource": source_name,
            "permissions": ["securitycenter.findings.update"],
        }
    )

    print(
        "Permision to create or update findings? {}".format(
            len(permission_response.permissions) > 0
        )
    )
    # [END test_iam_permissions]
    # [END securitycenter_test_iam]
    assert len(permission_response.permissions) > 0
    # [START securitycenter_test_iam]
    # [START test_iam_permissions]
    # Check for permissions necessary to call set_finding_state.
    permission_response = client.test_iam_permissions(
        request={
            "resource": source_name,
            "permissions": ["securitycenter.findings.setState"],
        }
    )
    print(
        "Permision to update state? {}".format(len(permission_response.permissions) > 0)
    )
    # [END test_iam_permissions]
    # [END securitycenter_test_iam]
    return permission_response
    assert len(permission_response.permissions) > 0


def list_all_findings(organization_id):
    # [START securitycenter_list_all_findings]
    # [START list_all_findings]
    from google.cloud import securitycenter

    # Create a client.
    client = securitycenter.SecurityCenterClient()

    # organization_id is the numeric ID of the organization. e.g.:
    # organization_id = "111122222444"
    org_name = "organizations/{org_id}".format(org_id=organization_id)
    # The "sources/-" suffix lists findings across all sources.  You
    # also use a specific source_name instead.
    all_sources = "{org_name}/sources/-".format(org_name=org_name)
    finding_result_iterator = client.list_findings(request={"parent": all_sources})
    for i, finding_result in enumerate(finding_result_iterator):
        print(
            "{}: name: {} resource: {}".format(
                i, finding_result.finding.name, finding_result.finding.resource_name
            )
        )
    # [END list_all_findings]
    # [END securitycenter_list_all_findings]
    return i


def list_filtered_findings(source_name):
    # [START securitycenter_list_filtered_findings]
    # [START list_filtered_findings]
    from google.cloud import securitycenter

    # Create a new client.
    client = securitycenter.SecurityCenterClient()

    # source_name is the resource path for a source that has been
    # created previously (you can use list_sources to find a specific one).
    # Its format is:
    # source_name = "organizations/{organization_id}/sources/{source_id}"
    # e.g.:
    # source_name = "organizations/111122222444/sources/1234"
    # You an also use a wild-card "-" for all sources:
    #   source_name = "organizations/111122222444/sources/-"
    finding_result_iterator = client.list_findings(
        request={"parent": source_name, "filter": 'category="MEDIUM_RISK_ONE"'}
    )
    # Iterate an print all finding names and the resource they are
    # in reference to.
    for i, finding_result in enumerate(finding_result_iterator):
        print(
            "{}: name: {} resource: {}".format(
                i, finding_result.finding.name, finding_result.finding.resource_name
            )
        )
    # [END list_filtered_findings]
    # [END securitycenter_list_filtered_findings]
    return i


def list_findings_at_time(source_name):
    # [START securitycenter_list_findings_at_time]
    # [START list_findings_at_a_time]
    from google.cloud import securitycenter
    from datetime import timedelta, datetime

    # Create a new client.
    client = securitycenter.SecurityCenterClient()

    # source_name is the resource path for a source that has been
    # created previously (you can use list_sources to find a specific one).
    # Its format is:
    # source_name = "organizations/{organization_id}/sources/{source_id}"
    # e.g.:
    # source_name = "organizations/111122222444/sources/1234"
    # You an also use a wild-card "-" for all sources:
    #   source_name = "organizations/111122222444/sources/-"
    five_days_ago = str(datetime.now() - timedelta(days=5))
    # [END list_findings_at_a_time]
    # [END securitycenter_list_findings_at_time]
    i = -1
    # [START securitycenter_list_findings_at_time]
    # [START list_findings_at_a_time]

    finding_result_iterator = client.list_findings(
        request={"parent": source_name, "filter": five_days_ago}
    )
    for i, finding_result in enumerate(finding_result_iterator):
        print(
            "{}: name: {} resource: {}".format(
                i, finding_result.finding.name, finding_result.finding.resource_name
            )
        )
    # [END list_findings_at_a_time]
    # [END securitycenter_list_findings_at_time]
    return i


def get_iam_policy(source_name):
    """Gives a user findingsEditor permission to the source."""
    # [START securitycenter_get_source_iam]
    # [START get_source_iam]
    from google.cloud import securitycenter

    client = securitycenter.SecurityCenterClient()

    # source_name is the resource path for a source that has been
    # created previously (you can use list_sources to find a specific one).
    # Its format is:
    # source_name = "organizations/{organization_id}/sources/{source_id}"
    # e.g.:
    # source_name = "organizations/111122222444/sources/1234"
    # Get the old policy so we can do an incremental update.
    policy = client.get_iam_policy(request={"resource": source_name})
    print("Policy: {}".format(policy))
    # [END get_source_iam]
    # [END securitycenter_get_source_iam]


def group_all_findings(organization_id):
    """Demonstrates grouping all findings across an organization."""
    i = 0
    # [START securitycenter_group_all_findings]
    # [START group_all_findings]
    from google.cloud import securitycenter

    # Create a client.
    client = securitycenter.SecurityCenterClient()

    # organization_id is the numeric ID of the organization. e.g.:
    # organization_id = "111122222444"
    org_name = "organizations/{org_id}".format(org_id=organization_id)
    # The "sources/-" suffix lists findings across all sources.  You
    # also use a specific source_name instead.
    all_sources = "{org_name}/sources/-".format(org_name=org_name)
    group_result_iterator = client.group_findings(
        request={"parent": all_sources, "group_by": "category"}
    )
    for i, group_result in enumerate(group_result_iterator):
        print((i + 1), group_result)
    # [END group_all_findings]
    # [END securitycenter_group_all_findings]
    return i


def group_filtered_findings(source_name):
    """Demonstrates grouping all findings across an organization."""
    i = 0
    # [START securitycenter_group_filtered_findings]
    from google.cloud import securitycenter

    # Create a client.
    client = securitycenter.SecurityCenterClient()

    # source_name is the resource path for a source that has been
    # created previously (you can use list_sources to find a specific one).
    # Its format is:
    # source_name = "organizations/{organization_id}/sources/{source_id}"
    # e.g.:
    # source_name = "organizations/111122222444/sources/1234"

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


def group_findings_at_time(source_name):
    """Demonstrates grouping all findings across an organization as of
    a specific time."""
    i = -1
    # [START securitycenter_group_findings_at_time]
    from datetime import datetime, timedelta
    from google.cloud import securitycenter

    # Create a client.
    client = securitycenter.SecurityCenterClient()

    # source_name is the resource path for a source that has been
    # created previously (you can use list_sources to find a specific one).
    # Its format is:
    # source_name = "organizations/{organization_id}/sources/{source_id}"
    # e.g.:
    # source_name = "organizations/111122222444/sources/1234"

    # Group findings as of yesterday.
    read_time = datetime.utcnow() - timedelta(days=1)

    group_result_iterator = client.group_findings(
        request={
            "parent": source_name,
            "group_by": "category",
            "read_time": read_time,
        }
    )
    for i, group_result in enumerate(group_result_iterator):
        print((i + 1), group_result)
    # [END securitycenter_group_findings_at_time]
    return i


def group_findings_and_changes(source_name):
    """Demonstrates grouping all findings across an organization and
    associated changes."""
    i = 0
    # [START securitycenter_group_findings_with_changes]
    from datetime import timedelta

    from google.cloud import securitycenter

    # Create a client.
    client = securitycenter.SecurityCenterClient()

    # source_name is the resource path for a source that has been
    # created previously (you can use list_sources to find a specific one).
    # Its format is:
    # source_name = "organizations/{organization_id}/sources/{source_id}"
    # e.g.:
    # source_name = "organizations/111122222444/sources/1234"

    # List assets and their state change the last 30 days
    compare_delta = timedelta(days=30)

    group_result_iterator = client.group_findings(
        request={
            "parent": source_name,
            "group_by": "state_change",
            "compare_duration": compare_delta,
        }
    )
    for i, group_result in enumerate(group_result_iterator):
        print((i + 1), group_result)
    # [END securitycenter_group_findings_with_changes]]
    return i
