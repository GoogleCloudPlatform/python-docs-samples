#!/usr/bin/env python
#
# Copyright 2020 Google LLC
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
"""Demos for working with notification configs."""


# [START securitycenter_create_notification_config]
def create_notification_config(parent_id, notification_config_id, pubsub_topic):
    """
    Args:
        parent_id: must be in one of the following formats:
            "organizations/{organization_id}"
            "projects/{project_id}"
            "folders/{folder_id}"
        notification_config_id: "your-config-id"
        pubsub_topic: "projects/{your-project-id}/topics/{your-topic-ic}"

    Ensure this ServiceAccount has the "pubsub.topics.setIamPolicy" permission on the new topic.
    """
    from google.cloud import securitycenter as securitycenter

    client = securitycenter.SecurityCenterClient()

    created_notification_config = client.create_notification_config(
        request={
            "parent": parent_id,
            "config_id": notification_config_id,
            "notification_config": {
                "description": "Notification for active findings",
                "pubsub_topic": pubsub_topic,
                "streaming_config": {"filter": 'state = "ACTIVE"'},
            },
        }
    )

    print(created_notification_config)
    # [END securitycenter_create_notification_config]
    return created_notification_config


# [START securitycenter_delete_notification_config]
def delete_notification_config(parent_id, notification_config_id):
    """
    Args:
        parent_id: must be in one of the following formats:
            "organizations/{organization_id}"
            "projects/{project_id}"
            "folders/{folder_id}"
        notification_config_id: "your-config-id"
    """
    from google.cloud import securitycenter as securitycenter

    client = securitycenter.SecurityCenterClient()

    notification_config_name = (
        f"{parent_id}/notificationConfigs/{notification_config_id}"
    )

    client.delete_notification_config(request={"name": notification_config_name})
    print(f"Deleted notification config: {notification_config_name}")
    # [END securitycenter_delete_notification_config]
    return True


# [START securitycenter_get_notification_config]
def get_notification_config(parent_id, notification_config_id):
    """
    Args:
        parent_id: must be in one of the following formats:
            "organizations/{organization_id}"
            "projects/{project_id}"
            "folders/{folder_id}"
        notification_config_id: "your-config-id"
    """
    from google.cloud import securitycenter as securitycenter

    client = securitycenter.SecurityCenterClient()

    notification_config_name = (
        f"{parent_id}/notificationConfigs/{notification_config_id}"
    )

    notification_config = client.get_notification_config(
        request={"name": notification_config_name}
    )
    print(f"Got notification config: {notification_config}")
    # [END securitycenter_get_notification_config]
    return notification_config


# [START securitycenter_list_notification_configs]
def list_notification_configs(parent_id):
    """
    Args:
        parent_id: must be in one of the following formats:
            "organizations/{organization_id}"
            "projects/{project_id}"
            "folders/{folder_id}"
    """
    from google.cloud import securitycenter as securitycenter

    client = securitycenter.SecurityCenterClient()

    notification_configs_iterator = client.list_notification_configs(
        request={"parent": parent_id}
    )
    for i, config in enumerate(notification_configs_iterator):
        print(f"{i}: notification_config: {config}")
    # [END securitycenter_list_notification_configs]]
    return notification_configs_iterator


# [START securitycenter_update_notification_config]
def update_notification_config(parent_id, notification_config_id, pubsub_topic):
    """
    Args:
        parent_id: must be in one of the following formats:
            "organizations/{organization_id}"
            "projects/{project_id}"
            "folders/{folder_id}"
        notification_config_id: "config-id-to-update"
        pubsub_topic: "projects/{new-project}/topics/{new-topic}"

    If updating a pubsub_topic, ensure this ServiceAccount has the
    "pubsub.topics.setIamPolicy" permission on the new topic.
    """
    from google.cloud import securitycenter as securitycenter
    from google.protobuf import field_mask_pb2

    client = securitycenter.SecurityCenterClient()

    notification_config_name = (
        f"{parent_id}/notificationConfigs/{notification_config_id}"
    )

    updated_description = "New updated description"
    updated_filter = 'state = "INACTIVE"'

    # Only description and pubsub_topic can be updated.
    field_mask = field_mask_pb2.FieldMask(
        paths=["description", "pubsub_topic", "streaming_config.filter"]
    )

    updated_notification_config = client.update_notification_config(
        request={
            "notification_config": {
                "name": notification_config_name,
                "description": updated_description,
                "pubsub_topic": pubsub_topic,
                "streaming_config": {"filter": updated_filter},
            },
            "update_mask": field_mask,
        }
    )

    print(updated_notification_config)
    # [END securitycenter_update_notification_config]
    return updated_notification_config
