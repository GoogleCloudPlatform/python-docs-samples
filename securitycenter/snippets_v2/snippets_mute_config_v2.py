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

from typing import Dict


# [START securitycenter_create_mute_config_v2]
def create_mute_rule(parent_path: str, location_id: str, mute_config_id: str) -> Dict:
    """
    Creates a mute configuration under a given scope that will mute
    all new findings that match a given filter.
    Existing findings will NOT BE muted.
    Args:
        parent_path: use any one of the following options:
                     - organizations/{organization_id}
                     - folders/{folder_id}
                     - projects/{project_id}
        location_id: Gcp location id; example: 'global'
        mute_config_id: Set a unique id; max of 63 chars.
    Returns:
        Dict: returns the mute rule details
    """

    from google.cloud import securitycenter_v2

    client = securitycenter_v2.SecurityCenterClient()

    mute_config = securitycenter_v2.MuteConfig()
    mute_config.description = "Mute low-medium IAM grants excluding 'compute' "
    # Set mute rule(s).
    # To construct mute rules and for supported properties, see:
    # https://cloud.google.com/security-command-center/docs/how-to-mute-findings#create_mute_rules
    mute_config.filter = (
        'severity="LOW" OR severity="MEDIUM" AND '
        'category="Persistence: IAM Anomalous Grant" AND '
        '-resource.type:"compute"'
    )
    mute_config.type = "STATIC"

    request = securitycenter_v2.CreateMuteConfigRequest()
    request.parent = parent_path + "/locations/" + location_id
    request.mute_config_id = mute_config_id
    request.mute_config = mute_config

    mute_config = client.create_mute_config(request=request)
    print(f"Mute rule created successfully: {mute_config.name}")
    return mute_config


# [END securitycenter_create_mute_config_v2]


# [START securitycenter_delete_mute_config_v2]
def delete_mute_rule(parent_path: str, location_id: str, mute_config_id: str) -> None:
    """
    Deletes a mute configuration given its resource name.
    Note: Previously muted findings are not affected when a mute config is deleted.
    Args:
         parent_path: use any one of the following options:
                     - organizations/{organization_id}
                     - folders/{folder_id}
                     - projects/{project_id}
        location_id: Gcp location id; example: 'global'
        mute_config_id: Set a unique id; max of 63 chars.
    Returns:
         None: returns none mute rule is deleted
    """
    from google.cloud import securitycenter_v2

    client = securitycenter_v2.SecurityCenterClient()

    request = securitycenter_v2.DeleteMuteConfigRequest()
    request.name = (
        parent_path + "/locations/" + location_id + "/muteConfigs/" + mute_config_id
    )

    client.delete_mute_config(request)
    print(f"Mute rule deleted successfully: {mute_config_id}")


# [END securitycenter_delete_mute_config_v2]


# [START securitycenter_get_mute_config_v2]
def get_mute_rule(parent_path: str, location_id: str, mute_config_id: str) -> Dict:
    """
    Retrieves a mute configuration given its resource name.
    Args:
        parent_path: use any one of the following options:
                     - organizations/{organization_id}
                     - folders/{folder_id}
                     - projects/{project_id}
        location_id: Gcp location id; example: 'global'
        mute_config_id: Set a unique id; max of 63 chars.
    Returns:
         Dict: returns the mute rule details
    """
    from google.cloud import securitycenter_v2

    client = securitycenter_v2.SecurityCenterClient()

    request = securitycenter_v2.GetMuteConfigRequest()
    request.name = (
        parent_path + "/locations/" + location_id + "/muteConfigs/" + mute_config_id
    )

    mute_config = client.get_mute_config(request)
    print(f"Retrieved the mute rule: {mute_config.name}")
    return mute_config


# [END securitycenter_get_mute_config_v2]


# [START securitycenter_list_mute_configs_v2]
def list_mute_rules(parent: str, location_id: str) -> Dict:
    """
    Listing mute configs at organization level will return all the configs
    at the org, folder and project levels.
    Similarly, listing configs at folder level will list all the configs
    at the folder and project levels.
    Args:
        parent: Use any one of the following resource paths to list mute configurations:
                - organizations/{organization_id}
                - folders/{folder_id}
                - projects/{project_id}
        location_id: Gcp location id; example: 'global'
    Returns:
         Dict: returns the mute rule details
    """
    from google.cloud import securitycenter_v2

    client = securitycenter_v2.SecurityCenterClient()

    request = securitycenter_v2.ListMuteConfigsRequest()
    request.parent = parent + "/locations/" + location_id
    response = client.list_mute_configs(request)
    # List all Mute Configs present in the resource.
    for mute_config in response:
        print(mute_config.name)
    return response


# [END securitycenter_list_mute_configs_v2]


# [START securitycenter_update_mute_config_v2]
def update_mute_rule(parent_path: str, location_id: str, mute_config_id: str) -> Dict:
    """
    Updates an existing mute configuration.
    The following can be updated in a mute config: description, and filter/ mute rule.
    Args:
        parent: Use any one of the following resource paths to list mute configurations:
                - organizations/{organization_id}
                - folders/{folder_id}
                - projects/{project_id}
        location_id: Gcp location id; example: 'global'
        mute_config_id: Set a unique id; max of 63 chars.
    Returns:
         Dict: returns the mute rule details
    """
    from google.cloud import securitycenter_v2
    from google.protobuf import field_mask_pb2

    client = securitycenter_v2.SecurityCenterClient()

    update_mute_config = securitycenter_v2.MuteConfig()
    update_mute_config.name = (
        parent_path + "/locations/" + location_id + "/muteConfigs/" + mute_config_id
    )
    update_mute_config.description = "Updated mute config description"

    field_mask = field_mask_pb2.FieldMask(paths=["description"])

    request = securitycenter_v2.UpdateMuteConfigRequest()
    request.mute_config = update_mute_config
    # Set the update mask to specify which properties of the Mute Config should be updated.
    # If empty, all mutable fields will be updated.
    # Make sure that the mask fields match the properties changed in 'update_mute_config'.
    # For more info on constructing update mask path, see the proto or:
    # https://cloud.google.com/security-command-center/docs/reference/rest/v1/folders.muteConfigs/patch?hl=en#query-parameters
    request.update_mask = field_mask

    mute_config = client.update_mute_config(request)
    print(f"Updated mute rule : {mute_config}")
    return mute_config


# [END securitycenter_update_mute_config_v2]
