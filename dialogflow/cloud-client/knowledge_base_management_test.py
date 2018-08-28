# Copyright 2018 Google LLC
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

import detect_intent_knowledge
import document_management
import knowledge_base_management

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
SESSION_ID = 'fake_session_for_testing'
TEXTS = ['Where is my data stored?']

KNOWLEDGE_BASE_NAME = 'fake_knowledge_base_name'
DOCUMENT_BASE_NAME = 'fake_document_name'


def test_create_knowledge_base(capsys):
    # Check the knowledge base does not yet exists
    knowledge_base_management.list_knowledge_bases(PROJECT_ID)

    out, _ = capsys.readouterr()
    assert 'Display Name: {}'.format(KNOWLEDGE_BASE_NAME) not in out

    # Create a knowledge base
    knowledge_base_management.create_knowledge_base(PROJECT_ID,
                                                    KNOWLEDGE_BASE_NAME)

    out, _ = capsys.readouterr()
    assert 'Display Name: {}'.format(KNOWLEDGE_BASE_NAME) in out

    # List the knowledge base
    knowledge_base_management.list_knowledge_bases(PROJECT_ID)

    out, _ = capsys.readouterr()
    assert 'Display Name: {}'.format(KNOWLEDGE_BASE_NAME) in out

    knowledge_base_id = out.split('knowledgeBases/')[1].rstrip()

    # Get the knowledge base
    knowledge_base_management.get_knowledge_base(PROJECT_ID, knowledge_base_id)

    out, _ = capsys.readouterr()
    assert 'Display Name: {}'.format(KNOWLEDGE_BASE_NAME) in out

    # Create a Document
    document_management.create_document(
        PROJECT_ID, knowledge_base_id, DOCUMENT_BASE_NAME, 'text/html', 'FAQ',
        'https://cloud.google.com/storage/docs/faq')

    out, _ = capsys.readouterr()
    assert 'Display Name: {}'.format(DOCUMENT_BASE_NAME) in out

    # List the Document
    document_management.list_documents(PROJECT_ID, knowledge_base_id)

    out, _ = capsys.readouterr()
    assert 'Display Name: {}'.format(DOCUMENT_BASE_NAME) in out

    document_id = out.split('documents/')[1].split(' - MIME Type:')[0].rstrip()

    # Get the Document
    document_management.get_document(PROJECT_ID, knowledge_base_id,
                                     document_id)

    out, _ = capsys.readouterr()
    assert 'Display Name: {}'.format(DOCUMENT_BASE_NAME) in out

    # Detect intent with Knowledge Base
    detect_intent_knowledge.detect_intent_knowledge(
        PROJECT_ID, SESSION_ID, 'en-us', knowledge_base_id, TEXTS)

    out, _ = capsys.readouterr()
    assert 'Knowledge results' in out

    # Delete the Document
    document_management.delete_document(PROJECT_ID, knowledge_base_id,
                                        document_id)

    # List the Document
    document_management.list_documents(PROJECT_ID, knowledge_base_id)

    out, _ = capsys.readouterr()
    assert 'Display Name: {}'.format(DOCUMENT_BASE_NAME) not in out

    # Delete the Knowledge Base
    knowledge_base_management.delete_knowledge_base(PROJECT_ID,
                                                    knowledge_base_id)

    # List the knowledge base
    knowledge_base_management.list_knowledge_bases(PROJECT_ID)

    out, _ = capsys.readouterr()
    assert 'Display Name: {}'.format(KNOWLEDGE_BASE_NAME) not in out
