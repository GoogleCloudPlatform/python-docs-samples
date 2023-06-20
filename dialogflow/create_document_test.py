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

from unittest import mock
import uuid

from google.cloud import dialogflow_v2beta1 as dialogflow
import pytest

import document_management
import test_utils

PROJECT_ID = "mock-dialogflow-project"
KNOWLEDGE_BASE_NAME = f"knowledge_{uuid.uuid4()}"
KNOWLEDGE_BASE_ID = uuid.uuid4().hex[0:27]
DOCUMENT_DISPLAY_NAME = f"test_document_{uuid.uuid4()}"
MIME_TYPE = "text/html"
KNOWLEDGE_TYPE = "FAQ"
CONTENT_URI = "https://cloud.google.com/storage/docs/faq"

CREATE_DOCUMENT_OPERATION = test_utils.create_mock_create_document_operation(
    DOCUMENT_DISPLAY_NAME,
    KNOWLEDGE_BASE_ID,
    MIME_TYPE,
    [getattr(dialogflow.Document.KnowledgeType, KNOWLEDGE_TYPE)],
    CONTENT_URI,
)


def test_create_document(capsys: pytest.CaptureFixture[str]):
    with mock.patch(
        "google.cloud.dialogflow_v2beta1.DocumentsClient.create_document",
        CREATE_DOCUMENT_OPERATION,
    ):
        document_management.create_document(
            PROJECT_ID,
            KNOWLEDGE_BASE_ID,
            DOCUMENT_DISPLAY_NAME,
            MIME_TYPE,
            KNOWLEDGE_TYPE,
            CONTENT_URI,
        )
        out, _ = capsys.readouterr()
        assert DOCUMENT_DISPLAY_NAME in out
