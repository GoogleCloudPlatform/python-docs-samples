# Copyright 2020 Google LLC
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

from __future__ import absolute_import

import os
import uuid

from google.cloud import dialogflow_v2
import pytest

import knowledge_base_management

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


@pytest.fixture(scope="function", autouse=True)
def teardown():
    yield

    # Delete the created knowledge base
    client = dialogflow_v2.KnowledgeBasesClient()
    assert pytest.KNOWLEDGE_BASE_ID is not None
    knowledge_base_path = client.knowledge_base_path(
        PROJECT_ID, pytest.KNOWLEDGE_BASE_ID
    )
    client.delete_knowledge_base(name=knowledge_base_path)


def test_create_knowledge_base():
    name = None

    try:
        kb_display_name = f"knowledge_{uuid.uuid4().hex}"
        (name, display_name) = knowledge_base_management.create_knowledge_base(
            PROJECT_ID, kb_display_name
        )
        assert kb_display_name == display_name
    except Exception as e:
        assert str(e) == ""

    if name is not None:
        client = dialogflow_v2.KnowledgeBasesClient()
        request = dialogflow_v2.DeleteKnowledgeBaseRequest(name=name)
        client.delete_knowledge_base(request=request)
