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

import create_conversation_with_ttl


@pytest.fixture
def project_id():
    _, project_id = google.auth.default()
    return project_id


@pytest.fixture
def conversation_resource(project_id):
    # Create a conversation
    conversation = create_conversation_with_ttl.create_conversation_with_ttl(project_id)
    yield conversation

    # Delete the conversation.
    insights_client = contact_center_insights_v1.ContactCenterInsightsClient()
    insights_client.delete_conversation(name=conversation.name)


def test_create_conversation_with_ttl(capsys, conversation_resource):
    conversation = conversation_resource
    out, err = capsys.readouterr()
    assert f"Created {conversation.name}" in out
