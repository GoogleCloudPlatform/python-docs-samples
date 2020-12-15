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

""" Examples of listing assets in Cloud Security Command Center."""


def list_all_assets(organization_id):
    """Demonstrate listing and printing all assets."""
    i = 0
    # [START securitycenter_demo_list_all_assets]
    # [START demo_list_all_assets]
    from google.cloud import securitycenter

    client = securitycenter.SecurityCenterClient()
    # organization_id is the numeric ID of the organization.
    # organization_id = "1234567777"
    org_name = "organizations/{org_id}".format(org_id=organization_id)

    # Call the API and print results.
    asset_iterator = client.list_assets(request={"parent": org_name})
    for i, asset_result in enumerate(asset_iterator):
        print(i, asset_result)
    # [END demo_list_all_assets]
    # [END securitycenter_demo_list_all_assets]
    return i


def list_assets_with_filters(organization_id):
    """Demonstrate listing assets with a filter."""
    i = 0
    # [START securitycenter_demo_list_assets_with_filter]
    # [START demo_list_assets_with_filter]
    from google.cloud import securitycenter

    client = securitycenter.SecurityCenterClient()

    # organization_id is the numeric ID of the organization.
    # organization_id = "1234567777"
    org_name = "organizations/{org_id}".format(org_id=organization_id)

    project_filter = (
        "security_center_properties.resource_type="
        + '"google.cloud.resourcemanager.Project"'
    )
    # Call the API and print results.
    asset_iterator = client.list_assets(
        request={"parent": org_name, "filter": project_filter}
    )
    for i, asset_result in enumerate(asset_iterator):
        print(i, asset_result)
    # [END demo_list_assets_with_filter]
    # [END securitycenter_demo_list_assets_with_filter]
    return i


def list_assets_with_filters_and_read_time(organization_id):
    """Demonstrate listing assets with a filter."""
    i = 0
    # [START securitycenter_demo_list_assets_with_filter_and_time]
    # [START demo_list_assets_with_filter_and_time]
    from datetime import datetime, timedelta

    from google.cloud import securitycenter

    client = securitycenter.SecurityCenterClient()

    # organization_id is the numeric ID of the organization.
    # organization_id = "1234567777"
    org_name = "organizations/{org_id}".format(org_id=organization_id)

    project_filter = (
        "security_center_properties.resource_type="
        + '"google.cloud.resourcemanager.Project"'
    )

    # Lists assets as of yesterday.
    read_time = datetime.utcnow() - timedelta(days=1)

    # Call the API and print results.
    asset_iterator = client.list_assets(
        request={
            "parent": org_name,
            "filter": project_filter,
            "read_time": read_time,
        }
    )
    for i, asset_result in enumerate(asset_iterator):
        print(i, asset_result)
    # [END demo_list_assets_with_filter_and_time]
    # [END securitycenter_demo_list_assets_with_filter_and_time]
    return i


def list_point_in_time_changes(organization_id):
    """Demonstrate listing assets along with their state changes."""
    i = 0
    # [START securitycenter_demo_list_assets_changes]
    # [START demo_list_assets_changes]
    from datetime import timedelta

    from google.cloud import securitycenter

    client = securitycenter.SecurityCenterClient()

    # organization_id is the numeric ID of the organization.
    # organization_id = "1234567777"
    org_name = "organizations/{org_id}".format(org_id=organization_id)
    project_filter = (
        "security_center_properties.resource_type="
        + '"google.cloud.resourcemanager.Project"'
    )

    # List assets and their state change the last 30 days
    compare_delta = timedelta(days=30)

    # Call the API and print results.
    asset_iterator = client.list_assets(
        request={
            "parent": org_name,
            "filter": project_filter,
            "compare_duration": compare_delta,
        }
    )
    for i, asset in enumerate(asset_iterator):
        print(i, asset)

    # [END demo_list_assets_changes]
    # [END securitycenter_demo_list_assets_changes]
    return i


def group_assets(organization_id):
    """Demonstrates grouping all assets by type. """
    i = 0
    # [START securitycenter_group_all_assets]
    from google.cloud import securitycenter

    client = securitycenter.SecurityCenterClient()

    # organization_id is the numeric ID of the organization.
    # organization_id = "1234567777"
    org_name = "organizations/{org_id}".format(org_id=organization_id)

    group_by_type = "security_center_properties.resource_type"

    result_iterator = client.group_assets(
        request={"parent": org_name, "group_by": group_by_type}
    )
    for i, result in enumerate(result_iterator):
        print((i + 1), result)
    # [END securitycenter_group_all_assets]
    return i


def group_filtered_assets(organization_id):
    """Demonstrates grouping assets by type with a filter. """
    i = 0
    # [START securitycenter_group_all_assets_with_filter]
    from google.cloud import securitycenter

    client = securitycenter.SecurityCenterClient()

    # organization_id is the numeric ID of the organization.
    # organization_id = "1234567777"
    org_name = "organizations/{org_id}".format(org_id=organization_id)

    group_by_type = "security_center_properties.resource_type"
    only_projects = (
        "security_center_properties.resource_type="
        + '"google.cloud.resourcemanager.Project"'
    )
    result_iterator = client.group_assets(
        request={"parent": org_name, "group_by": group_by_type, "filter": only_projects}
    )
    for i, result in enumerate(result_iterator):
        print((i + 1), result)
    # [END securitycenter_group_all_assets_with_filter]
    # only one asset type is a project
    return i


def group_assets_by_changes(organization_id):
    """Demonstrates grouping assets by their changes over a period of time."""
    i = 0
    # [START securitycenter_group_all_assets_by_change]
    from datetime import timedelta

    from google.cloud import securitycenter

    client = securitycenter.SecurityCenterClient()

    duration = timedelta(days=5)

    # organization_id is the numeric ID of the organization.
    # organization_id = "1234567777"
    org_name = "organizations/{org_id}".format(org_id=organization_id)
    result_iterator = client.group_assets(
        request={
            "parent": org_name,
            "group_by": "state_change",
            "compare_duration": duration,
        }
    )
    for i, result in enumerate(result_iterator):
        print((i + 1), result)
    # [END securitycenter_group_all_assets_by_change]
    return i
