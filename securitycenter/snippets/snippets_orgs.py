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
"""Examples for working with organization settings. """


def get_settings(organization_id):
    """Example showing how to retreive current organization settings."""
    # [START get_org_settings]
    from google.cloud import securitycenter

    client = securitycenter.SecurityCenterClient()
    # organization_id is numeric ID for the organization. e.g.
    # organization_id = "111112223333"

    org_settings_name = client.organization_settings_path(organization_id)

    org_settings = client.get_organization_settings(request={"name": org_settings_name})
    print(org_settings)
    # [END get_org_settings]


def update_asset_discovery_org_settings(organization_id):
    """Example showing how to update the asset discovery configuration
    for an organization."""
    # [START update_org_settings]
    from google.cloud import securitycenter
    from google.protobuf import field_mask_pb2

    # Create the client
    client = securitycenter.SecurityCenterClient()
    # organization_id is numeric ID for the organization. e.g.
    # organization_id = "111112223333"
    org_settings_name = "organizations/{org_id}/organizationSettings".format(
        org_id=organization_id
    )
    # Only update the enable_asset_discovery_value (leave others untouched).
    field_mask = field_mask_pb2.FieldMask(paths=["enable_asset_discovery"])
    # Call the service.
    updated = client.update_organization_settings(
        request={
            "organization_settings": {
                "name": org_settings_name,
                "enable_asset_discovery": True,
            },
            "update_mask": field_mask,
        }
    )
    print("Asset Discovery Enabled? {}".format(updated.enable_asset_discovery))
    # [END update_org_settings]
    return updated
