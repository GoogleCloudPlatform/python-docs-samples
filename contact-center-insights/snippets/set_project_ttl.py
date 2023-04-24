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
# Set a project-level TTL for all incoming conversations.
# [START contactcenterinsights_set_project_ttl]
from google.api_core import protobuf_helpers
from google.cloud import contact_center_insights_v1
from google.protobuf import duration_pb2


def set_project_ttl(project_id: str) -> None:
    """Sets a project-level TTL for all incoming conversations.

    Args:
        project_id:
            The project identifier. For example, 'my-project'.

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

    conversation_ttl = duration_pb2.Duration()
    conversation_ttl.seconds = 86400
    settings.conversation_ttl = conversation_ttl

    # Construct an update mask to only update the fields that are set on the settings resource.
    update_mask = protobuf_helpers.field_mask(None, type(settings).pb(settings))

    # Construct an Insights client that will authenticate via Application Default Credentials.
    # See authentication details at https://cloud.google.com/docs/authentication/production.
    insights_client = contact_center_insights_v1.ContactCenterInsightsClient()

    # Call the Insights client to set a project-level TTL.
    insights_client.update_settings(settings=settings, update_mask=update_mask)

    # Call the Insights client to get the project-level TTL to confirm that it was set.
    new_conversation_ttl = insights_client.get_settings(
        name=settings.name
    ).conversation_ttl
    print(
        "Set TTL for all incoming conversations to {} day".format(
            new_conversation_ttl.days
        )
    )


# [END contactcenterinsights_set_project_ttl]
