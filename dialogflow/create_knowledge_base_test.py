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

from google.cloud import dialogflow_v2beta1
import pytest

import knowledge_base_management

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
KNOWLEDGE_BASE_NAME = "knowledge_{}".format(uuid.uuid4())
pytest.KNOWLEDGE_BASE_ID = None


@pytest.fixture(scope="function", autouse=True)
def teardown():
    yield

    # Delete the created knowledge base
    client = dialogflow_v2beta1.KnowledgeBasesClient()
    assert pytest.KNOWLEDGE_BASE_ID is not None
    knowledge_base_path = client.knowledge_base_path(
        PROJECT_ID, pytest.KNOWLEDGE_BASE_ID
    )
    client.delete_knowledge_base(name=knowledge_base_path)


def test_create_knowledge_base(capsys):
    knowledge_base_management.create_knowledge_base(PROJECT_ID, KNOWLEDGE_BASE_NAME)
    out, _ = capsys.readouterr()
    assert KNOWLEDGE_BASE_NAME in out

    pytest.KNOWLEDGE_BASE_ID = out.split("/knowledgeBases/")[1].split("\n")[0]
