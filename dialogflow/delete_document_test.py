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

import dialogflow_v2beta1 as dialogflow
import pytest

import document_management

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
KNOWLEDGE_BASE_NAME = 'knowledge_{}'.format(uuid.uuid4())
DOCUMENT_DISPLAY_NAME = 'test_document_{}'.format(uuid.uuid4())
pytest.KNOWLEDGE_BASE_ID = None
pytest.DOCUMENT_ID = None


@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    # Create a knowledge base to use in document management
    client = dialogflow.KnowledgeBasesClient()
    project_path = client.project_path(PROJECT_ID)
    knowledge_base = dialogflow.types.KnowledgeBase(
        display_name=KNOWLEDGE_BASE_NAME)
    response = client.create_knowledge_base(project_path, knowledge_base)
    pytest.KNOWLEDGE_BASE_ID = response.name.split(
        '/knowledgeBases/')[1].split('\n')[0]

    # Create a document to delete
    knowledge_base_path = client.knowledge_base_path(
        PROJECT_ID, pytest.KNOWLEDGE_BASE_ID)
    document = dialogflow.types.Document(
        display_name=DOCUMENT_DISPLAY_NAME, mime_type='text/html',
        content_uri='https://cloud.google.com/storage/docs/faq')
    document.knowledge_types.append(
        dialogflow.types.Document.KnowledgeType.Value('FAQ'))
    documents_client = dialogflow.DocumentsClient()
    response = documents_client.create_document(knowledge_base_path, document)
    document = response.result(timeout=90)
    pytest.DOCUMENT_ID = document.name.split('/documents/')[1].split('\n')[0]

    yield

    # Delete the created knowledge base
    client.delete_knowledge_base(knowledge_base_path, force=True)


def test_delete_document(capsys):
    document_management.delete_document(
        PROJECT_ID, pytest.KNOWLEDGE_BASE_ID, pytest.DOCUMENT_ID)
    document_management.list_documents(PROJECT_ID, pytest.KNOWLEDGE_BASE_ID)
    out, _ = capsys.readouterr()
    assert DOCUMENT_DISPLAY_NAME not in out
