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

import get_operation

TRANSCRIPT_URI = "gs://cloud-samples-data/ccai/chat_sample.json"
AUDIO_URI = "gs://cloud-samples-data/ccai/voice_6912.txt"


@pytest.fixture
def project_id():
    _, project_id = google.auth.default()
    return project_id


@pytest.fixture
def insights_client():
    return contact_center_insights_v1.ContactCenterInsightsClient()


@pytest.fixture
def conversation_resource(project_id, insights_client):
    # Create a conversation.
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
def analysis_operation(conversation_resource, insights_client):
    # Create an analysis.
    conversation_name = conversation_resource.name
    analysis = contact_center_insights_v1.Analysis()
    analysis_operation = insights_client.create_analysis(
        parent=conversation_name, analysis=analysis
    )

    # Wait until the analysis operation is done and return the operation.
    analysis_operation.result(timeout=600)
    yield analysis_operation


def test_get_operation(capsys, analysis_operation):
    operation_name = analysis_operation.operation.name
    get_operation.get_operation(operation_name)
    out, err = capsys.readouterr()
    assert "Operation is done" in out
