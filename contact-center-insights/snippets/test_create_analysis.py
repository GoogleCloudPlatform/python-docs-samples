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
import google.auth
from google.cloud import contact_center_insights_v1
import pytest

import create_analysis

TRANSCRIPT_URI = "gs://cloud-samples-data/ccai/chat_sample.json"
AUDIO_URI = "gs://cloud-samples-data/ccai/voice_6912.txt"


@pytest.fixture
def project_id():
    _, project_id = google.auth.default()
    return project_id


@pytest.fixture
def conversation_resource(project_id):
    # Create a conversation.
    insights_client = contact_center_insights_v1.ContactCenterInsightsClient()

    parent = (
        contact_center_insights_v1.ContactCenterInsightsClient.common_location_path(
            project_id, "us-central1"
        )
    )

    conversation = contact_center_insights_v1.Conversation()
    conversation.data_source.gcs_source.transcript_uri = TRANSCRIPT_URI
    conversation.data_source.gcs_source.audio_uri = AUDIO_URI
    conversation.medium = contact_center_insights_v1.Conversation.Medium.CHAT

    conversation = insights_client.create_conversation(
        parent=parent, conversation=conversation
    )
    yield conversation

    # Delete the conversation.
    delete_request = contact_center_insights_v1.DeleteConversationRequest()
    delete_request.name = conversation.name
    delete_request.force = True
    insights_client.delete_conversation(request=delete_request)


@pytest.fixture
def analysis_resource(conversation_resource):
    conversation_name = conversation_resource.name
    yield create_analysis.create_analysis(conversation_name)


def test_create_analysis(capsys, analysis_resource):
    analysis = analysis_resource
    out, err = capsys.readouterr()
    assert f"Created {analysis.name}" in out
