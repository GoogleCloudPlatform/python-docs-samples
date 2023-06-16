# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import mock

from google.api_core.operation import Operation
from google.cloud import dialogflow_v2beta1 as dialogflow


def create_mock_conversation(display_name, name):
    conversation = mock.MagicMock(spec=dialogflow.Conversation)
    conversation.display_name = display_name
    conversation.name = name
    return conversation


def create_mock_create_document_operation(
    document_display_name, name, mime_type, knowledge_types, content_uri
):
    operation = mock.MagicMock(spec=Operation)
    document = create_mock_document(
        document_display_name, name, mime_type, knowledge_types, content_uri
    )
    operation.result = document
    return mock.MagicMock(return_value=operation)


def create_mock_document(
    document_display_name, name, mime_type, knowledge_types, content_uri
):
    document = mock.MagicMock(spec=dialogflow.Document)
    document.display_name = document_display_name
    document.name = name
    document.mime_type = mime_type
    document.knowledge_types = knowledge_types
    document.content_uri = content_uri
    return mock.MagicMock(return_value=document)


# def create_analyze_text_response():
#     mock.
