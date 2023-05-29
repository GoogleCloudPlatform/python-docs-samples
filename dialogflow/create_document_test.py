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
from unittest import mock
import uuid

from google.cloud import dialogflow_v2beta1 as dialogflow
import pytest

import document_management
import test_utils

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
KNOWLEDGE_BASE_NAME = f"knowledge_{uuid.uuid4()}"
DOCUMENT_DISPLAY_NAME = f"test_document_{uuid.uuid4()}"
MIME_TYPE = "text/html"
KNOWLEDGE_TYPE = "FAQ"
CONTENT_URI = "https://cloud.google.com/storage/docs/faq"


@pytest.fixture(scope="function")
def mock_create_document_operation():
    return test_utils.create_mock_create_document_operation(
        DOCUMENT_DISPLAY_NAME,
        knowledge_base_id,
        MIME_TYPE,
        [getattr(dialogflow.Document.KnowledgeType, KNOWLEDGE_TYPE)],
        CONTENT_URI
    )


@pytest.fixture(scope="function")
def knowledge_base_id():
    # Create a knowledge base to use in document management
    client = dialogflow.KnowledgeBasesClient()
    project_path = client.common_project_path(PROJECT_ID)
    knowledge_base = dialogflow.KnowledgeBase(display_name=KNOWLEDGE_BASE_NAME)
    response = client.create_knowledge_base(
        parent=project_path, knowledge_base=knowledge_base
    )
    knowledge_base_id = response.name.split("/knowledgeBases/")[1].split("\n")[0]

    yield knowledge_base_id

    # Delete the created knowledge base
    knowledge_base_path = client.knowledge_base_path(PROJECT_ID, knowledge_base_id)
    request = dialogflow.DeleteKnowledgeBaseRequest(
        name=knowledge_base_path, force=True
    )
    client.delete_knowledge_base(request=request)


def test_create_document(
    capsys: pytest.CaptureFixture[str],
    knowledge_base_id: str,
    mock_create_document_operation: mock.MagicMock,
):
    with mock.patch(
        "document_management.dialogflow.DocumentsClient.create_document",
        mock_create_document_operation,
    ):
        document_management.create_document(
            PROJECT_ID,
            knowledge_base_id,
            DOCUMENT_DISPLAY_NAME,
            MIME_TYPE,
            KNOWLEDGE_TYPE,
            CONTENT_URI,
        )
        out, _ = capsys.readouterr()
        assert DOCUMENT_DISPLAY_NAME in out
