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


def create_notification_config(organization_id, notification_config_id, pubsub_topic):

    # [START scc_create_notification_config]
    from google.cloud import securitycenter as securitycenter

    client = securitycenter.SecurityCenterClient()

    # TODO: organization_id = "your-org-id"
    # TODO: notification_config_id = "your-config-id"
    # TODO: pubsub_topic = "projects/{your-project-id}/topics/{your-topic-ic}"
    # Ensure this ServiceAccount has the "pubsub.topics.setIamPolicy" permission on the new topic.

    org_name = "organizations/{org_id}".format(org_id=organization_id)

    created_notification_config = client.create_notification_config(
        org_name,
        notification_config_id,
        {
            "description": "Notification for active findings",
            "pubsub_topic": pubsub_topic,
            "streaming_config": {"filter": 'state = "ACTIVE"'},
        },
    )

    print(created_notification_config)
    # [END scc_create_notification_config]
    return created_notification_config


def delete_notification_config(organization_id, notification_config_id):

    # [START scc_delete_notification_config]
    from google.cloud import securitycenter as securitycenter

    client = securitycenter.SecurityCenterClient()

    # TODO: organization_id = "your-org-id"
    # TODO: notification_config_id = "your-config-id"

    notification_config_name = "organizations/{org_id}/notificationConfigs/{config_id}".format(
        org_id=organization_id, config_id=notification_config_id
    )

    client.delete_notification_config(notification_config_name)
    print("Deleted notification config: {}".format(notification_config_name))
    # [END scc_delete_notification_config]
    return True


def get_notification_config(organization_id, notification_config_id):

    # [START scc_get_notification_config]
    from google.cloud import securitycenter as securitycenter

    client = securitycenter.SecurityCenterClient()

    # TODO: organization_id = "your-org-id"
    # TODO: notification_config_id = "your-config-id"

    notification_config_name = "organizations/{org_id}/notificationConfigs/{config_id}".format(
        org_id=organization_id, config_id=notification_config_id
    )

    notification_config = client.get_notification_config(notification_config_name)
    print("Got notification config: {}".format(notification_config))
    # [END scc_get_notification_config]
    return notification_config


def list_notification_configs(organization_id):

    # [START scc_list_notification_configs]
    from google.cloud import securitycenter as securitycenter

    client = securitycenter.SecurityCenterClient()

    # TODO: organization_id = "your-org-id"
    org_name = "organizations/{org_id}".format(org_id=organization_id)

    notification_configs_iterator = client.list_notification_configs(org_name)
    for i, config in enumerate(notification_configs_iterator):
        print("{}: notification_config: {}".format(i, config))
    # [END scc_list_notification_configs]
    return notification_configs_iterator


def update_notification_config(organization_id, notification_config_id, pubsub_topic):
    # [START scc_update_notification_config]
    from google.cloud import securitycenter as securitycenter
    from google.protobuf import field_mask_pb2

    client = securitycenter.SecurityCenterClient()

    # TODO organization_id = "your-org-id"
    # TODO notification_config_id = "config-id-to-update"
    # TODO pubsub_topic = "projects/{new-project}/topics/{new-topic}"
    # If updating a pubsub_topic, ensure this ServiceAccount has the
    # "pubsub.topics.setIamPolicy" permission on the new topic.

    notification_config_name = "organizations/{org_id}/notificationConfigs/{config_id}".format(
        org_id=organization_id, config_id=notification_config_id
    )

    updated_description = "New updated description"

    # Only description and pubsub_topic can be updated.
    field_mask = field_mask_pb2.FieldMask(paths=["description", "pubsub_topic"])

    updated_notification_config = client.update_notification_config(
        {
            "name": notification_config_name,
            "description": updated_description,
            "pubsub_topic": pubsub_topic,
        },
        update_mask=field_mask,
    )

    print(updated_notification_config)
    # [END scc_update_notification_config]
    return updated_notification_config
