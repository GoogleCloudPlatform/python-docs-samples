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
"""Demos for working with notification configs."""
from google.cloud.securitycenter_v2 import (
    ListNotificationConfigsResponse,
    NotificationConfig,
)


# [START securitycenter_create_notification_config_v2]
def create_notification_config(
    parent_id, location_id, pubsub_topic, notification_config_id
) -> NotificationConfig:
    """
    This method is used to create the Notification Config.
    Args:
        parent_id: must be in one of the following formats:
            "organizations/{organization_id}"
            "projects/{project_id}"
            "folders/{folder_id}"
        location_id: "global"
        pubsub_topic: "projects/{your-project-id}/topics/{your-topic-id}"
        notification_config_id: "your-config-id"


    Ensure this ServiceAccount has the "pubsub.topics.setIamPolicy" permission on the new topic.
    """
    from google.cloud import securitycenter_v2 as securitycenter_v2

    client = securitycenter_v2.SecurityCenterClient()
    parent_id = parent_id + "/locations/" + location_id
    response = client.create_notification_config(
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
    print(f"create notification config response:{response}")
    return response


# [END securitycenter_create_notification_config_v2]


# [START securitycenter_delete_notification_config_v2]
def delete_notification_config(parent_id, location_id, notification_config_id) -> bool:
    """
    This method is used to delete the Notification Config.
    Args:
        parent_id: must be in one of the following formats:
            "organizations/{organization_id}"
            "projects/{project_id}"
            "folders/{folder_id}"
        location_id: "global"
        notification_config_id: "your-config-id"
    """
    from google.cloud import securitycenter_v2 as securitycenter_v2

    client = securitycenter_v2.SecurityCenterClient()
    parent_id = parent_id + "/locations/" + location_id
    notification_config_name = (
        f"{parent_id}/notificationConfigs/{notification_config_id}"
    )

    client.delete_notification_config(request={"name": notification_config_name})
    print(f"Deleted notification config: {notification_config_name}")
    # [END securitycenter_delete_notification_config_v2]


# [START securitycenter_get_notification_config_v2]
def get_notification_config(
    parent_id, location_id, notification_config_id
) -> NotificationConfig:
    """
    This method is used to get the Notification Config.
    Args:
        parent_id: must be in one of the following formats:
            "organizations/{organization_id}"
            "projects/{project_id}"
            "folders/{folder_id}"
        location_id: "global"
        notification_config_id: "your-config-id"
    """
    from google.cloud import securitycenter_v2 as securitycenter_v2

    client = securitycenter_v2.SecurityCenterClient()
    parent_id = parent_id + "/locations/" + location_id
    notification_config_name = (
        f"{parent_id}/notificationConfigs/{notification_config_id}"
    )

    response = client.get_notification_config(
        request={"name": notification_config_name}
    )
    print(f"Got notification config: {response}")
    return response


# [END securitycenter_get_notification_config_v2]


# [START securitycenter_list_notification_configs_v2]
def list_notification_configs(
    parent_id, location_id
) -> ListNotificationConfigsResponse:
    """
    This method is used to list the Notification Config.
    Args:
        parent_id: must be in one of the following formats:
            "organizations/{organization_id}"
            "projects/{project_id}"
            "folders/{folder_id}"
        location_id: "global"
    """
    from google.cloud import securitycenter_v2 as securitycenter_v2

    all_config = []
    client = securitycenter_v2.SecurityCenterClient()
    parent_id = parent_id + "/locations/" + location_id
    notification_configs_iterator = client.list_notification_configs(
        request={"parent": parent_id, "page_size": 1000}
    )
    for i, config in enumerate(notification_configs_iterator):
        all_config.append(config)
    next_page_token = notification_configs_iterator.next_page_token
    while next_page_token:
        iterator = client.list_notification_configs(
            request={
                "parent": parent_id,
                "page_token": next_page_token,
                "page_size": 1000,
            }
        )
        for i, config in enumerate(iterator):
            all_config.append(config)
    print(all_config)
    return all_config


# [END securitycenter_list_notification_configs_v2]


# [START securitycenter_update_notification_config_v2]
def update_notification_config(
    parent_id, location_id, pubsub_topic, notification_config_id
) -> NotificationConfig:
    """
    This method is used to update the Notification Config.
    Args:
        parent_id: must be in one of the following formats:
            "organizations/{organization_id}"
            "projects/{project_id}"
            "folders/{folder_id}"
        location_id: "global"
        pubsub_topic: "projects/{new-project}/topics/{new-topic}"
        notification_config_id: "config-id-to-update"


    If updating a pubsub_topic, ensure this ServiceAccount has the
    "pubsub.topics.setIamPolicy" permission on the new topic.
    """
    from google.cloud import securitycenter_v2 as securitycenter_v2
    from google.protobuf import field_mask_pb2

    client = securitycenter_v2.SecurityCenterClient()
    parent_id = parent_id + "/locations/" + location_id
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
    return updated_notification_config


# [END securitycenter_update_notification_config_v2]


# [START securitycenter_receive_notifications_v2]
def receive_notifications(subscription_name) -> bool:
    # Requires https://cloud.google.com/pubsub/docs/quickstart-client-libraries#pubsub-client-libraries-python
    import concurrent

    from google.cloud import pubsub_v1
    from google.cloud.securitycenter_v2 import NotificationMessage

    """
    This method is used to receive the Notification Config.
    Args:
        subscription_name: "projects/{your-project-id}/subscriptions/{your-subscription-id}"
    """

    def callback(message):
        try:
            # Print the data received for debugging purpose if needed
            print(f"Received message: {message.data}")

            notification_msg = NotificationMessage.from_json(message.data)
            print(
                "Notification config name: {}".format(
                    notification_msg.notification_config_name
                )
            )
            print(f"Finding: {notification_msg.finding}")

            # Ack the message to prevent it from being pulled again
            message.ack()
        except Exception as e:
            print(f"couldn't pass message {e}")

    subscriber = pubsub_v1.SubscriberClient()

    streaming_pull_future = subscriber.subscribe(subscription_name, callback=callback)

    print(f"Listening for messages on {subscription_name}...\n")
    try:
        streaming_pull_future.result(timeout=10)  # Block for 1 second
    except concurrent.futures.TimeoutError:
        streaming_pull_future.cancel()
    return True


# [END securitycenter_receive_notifications_v2]
