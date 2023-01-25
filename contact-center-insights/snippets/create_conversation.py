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
# [START contactcenterinsights_create_conversation]
from google.cloud import contact_center_insights_v1


def create_conversation(
    project_id: str,
    transcript_uri: str = "gs://cloud-samples-data/ccai/chat_sample.json",
    audio_uri: str = "gs://cloud-samples-data/ccai/voice_6912.txt",
) -> contact_center_insights_v1.Conversation:
    """Creates a conversation.

    Args:
        project_id:
            The project identifier. For example, 'my-project'.
        transcript_uri:
            The Cloud Storage URI that points to a file that contains the
            conversation transcript. Format is 'gs://{bucket_name}/{file.json}'.
            For example, 'gs://cloud-samples-data/ccai/chat_sample.json'.
        audio_uri:
            The Cloud Storage URI that points to a file that contains the
            conversation audio. Format is 'gs://{bucket_name}/{file.json}'.
            For example, 'gs://cloud-samples-data/ccai/voice_6912.txt'.

    Returns:
        A conversation.
    """
    # Construct a parent resource.
    parent = (
        contact_center_insights_v1.ContactCenterInsightsClient.common_location_path(
            project_id, "us-central1"
        )
    )

    # Construct a conversation.
    conversation = contact_center_insights_v1.Conversation()
    conversation.data_source.gcs_source.transcript_uri = transcript_uri
    conversation.data_source.gcs_source.audio_uri = audio_uri
    conversation.medium = contact_center_insights_v1.Conversation.Medium.CHAT

    # Call the Insights client to create a conversation.
    insights_client = contact_center_insights_v1.ContactCenterInsightsClient()
    conversation = insights_client.create_conversation(
        parent=parent, conversation=conversation
    )

    print(f"Created {conversation.name}")
    return conversation


# [END contactcenterinsights_create_conversation]
