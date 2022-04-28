# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# [START contactcenterinsights_enable_pubsub_notifications]
from google.api_core import protobuf_helpers
from google.cloud import contact_center_insights_v1


def enable_pubsub_notifications(
    project_id: str, topic_create_conversation: str, topic_create_analysis: str
) -> None:
    """Enables Cloud Pub/Sub notifications for specified events.

    Args:
        project_id:
            The project identifier. For example, 'my-project'.
        topic_create_conversation:
            The Cloud Pub/Sub topic to notify of conversation creation events.
            Format is 'projects/{project_id}/topics/{topic_id}'.
            For example, 'projects/my-project/topics/my-topic'.
        topic_create_analysis:
            The Cloud Pub/Sub topic to notify of analysis creation events.
            Format is 'projects/{project_id}/topics/{topic_id}'.
            For example, 'projects/my-project/topics/my-topic'.

    Returns:
        None.
    """
    # Construct a settings resource.
    settings = contact_center_insights_v1.Settings()
    settings.name = (
        contact_center_insights_v1.ContactCenterInsightsClient.settings_path(
            project_id, "us-central1"
        )
    )
    settings.pubsub_notification_settings = {
        "create-conversation": topic_create_conversation,
        "create-analysis": topic_create_analysis,
    }

    update_mask = protobuf_helpers.field_mask(None, type(settings).pb(settings))

    # Call the Insights client to enable Pub/Sub notifications.
    insights_client = contact_center_insights_v1.ContactCenterInsightsClient()
    insights_client.update_settings(settings=settings, update_mask=update_mask)
    print("Enabled Pub/Sub notifications")


# [END contactcenterinsights_enable_pubsub_notifications]
