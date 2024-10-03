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
"""Demos for working with security marks."""
from typing import Dict


# [START securitycenter_add_security_marks_v2]
def add_to_asset(organization_id, asset_name) -> Dict:
    """
    Add new security marks to an asset.
    Args:
       organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
       asset_name: is the resource path for an asset that exists in SCC

    Returns:
        Dict: returns the updated security marks details.
    """
    from google.cloud import securitycenter_v2
    from google.protobuf import field_mask_pb2

    # Create a new client.
    client = securitycenter_v2.SecurityCenterClient()
    asset_name = f"organizations/{organization_id}/assets/{asset_name}"
    marks_name = f"{asset_name}/securityMarks"

    # Notice the suffix after "marks." in the field mask matches the keys
    # in marks.
    field_mask = field_mask_pb2.FieldMask(paths=["marks.key_a", "marks.key_b"])
    marks = {"key_a": "value_a", "key_b": "value_b"}

    updated_marks = client.update_security_marks(
        request={
            "security_marks": {"name": marks_name, "marks": marks},
            "update_mask": field_mask,
        }
    )
    print(updated_marks)
    return updated_marks, marks


# [END securitycenter_add_security_marks_v2]


# [START securitycenter_delete_security_marks_v2]
def delete_security_marks(organization_id, asset_name) -> Dict:
    """
    Removes security marks from an asset.
    Args:
       organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
       asset_name: is the resource path for an asset that exists in SCC

    Returns:
        Dict: returns the deleted security marks response.
    """
    # Make sure they are there first
    add_to_asset(organization_id, asset_name)
    from google.cloud import securitycenter_v2
    from google.protobuf import field_mask_pb2

    # Create a new client.
    client = securitycenter_v2.SecurityCenterClient()
    asset_name = f"organizations/{organization_id}/assets/{asset_name}"
    marks_name = f"{asset_name}/securityMarks"

    field_mask = field_mask_pb2.FieldMask(paths=["marks.key_a", "marks.key_b"])

    updated_marks = client.update_security_marks(
        request={
            "security_marks": {
                "name": marks_name
                # Note, no marks specified, so the specified values in
                # the fields masks will be deleted.
            },
            "update_mask": field_mask,
        }
    )
    print(updated_marks)
    return updated_marks


# [END securitycenter_delete_security_marks_v2]


# [START securitycenter_add_delete_security_marks_v2]
def delete_and_update_marks(organization_id, asset_name) -> Dict:
    """
    Updates and deletes security marks from an asset in the same call.
    Args:
       organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
       asset_name: is the resource path for an asset that exists in SCC

    Returns:
        Dict: returns the deleted security marks response.

    """
    # Make sure they are there first
    add_to_asset(organization_id, asset_name)
    from google.cloud import securitycenter_v2
    from google.protobuf import field_mask_pb2

    client = securitycenter_v2.SecurityCenterClient()
    asset_name = f"organizations/{organization_id}/assets/{asset_name}"
    marks_name = f"{asset_name}/securityMarks"

    field_mask = field_mask_pb2.FieldMask(paths=["marks.key_a", "marks.key_b"])
    marks = {"key_a": "new_value_for_a"}

    updated_marks = client.update_security_marks(
        request={
            "security_marks": {"name": marks_name, "marks": marks},
            "update_mask": field_mask,
        }
    )
    print(updated_marks)
    return updated_marks


# [END securitycenter_add_delete_security_marks_v2]


# [START securitycenter_add_finding_security_marks_v2]
def add_to_finding(organization_id, source_name, location_id, finding_name):
    """
    Adds security marks to a finding.
    Args:
       organization_id: organization_id is the numeric ID of the organization. e.g.:organization_id = "111122222444"
       source_name: is the resource path for a source that has been created
       location_id: Gcp location id; example: 'global'
       finding_name: finding name to add security marks.

    Returns:
        Dict: returns the deleted security marks response.
    """
    from google.cloud import securitycenter_v2
    from google.protobuf import field_mask_pb2

    client = securitycenter_v2.SecurityCenterClient()
    finding_name = f"organizations/{organization_id}/sources/{source_name}/locations/{location_id}/findings/{finding_name}"
    finding_marks_name = f"{finding_name}/securityMarks"

    # Notice the suffix after "marks." in the field mask matches the keys
    # in marks.
    field_mask = field_mask_pb2.FieldMask(
        paths=["marks.finding_key_a", "marks.finding_key_b"]
    )
    marks = {"finding_key_a": "value_a", "finding_key_b": "value_b"}

    updated_marks = client.update_security_marks(
        request={
            "security_marks": {"name": finding_marks_name, "marks": marks},
            "update_mask": field_mask,
        }
    )
    return updated_marks, marks


# [END securitycenter_add_finding_security_marks_v2]
