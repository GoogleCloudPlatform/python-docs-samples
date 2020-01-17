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

import datetime
import os

import dialogflow_v2beta1 as dialogflow
import pytest

import knowledge_base_management

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
KNOWLEDGE_BASE_NAME = 'knowledge_' \
                      + datetime.datetime.now().strftime("%Y%m%d%H%M%S")


@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    # Create a knowledge base to list
    client = dialogflow.KnowledgeBasesClient()
    project_path = client.project_path(PROJECT_ID)
    knowledge_base = dialogflow.types.KnowledgeBase(
        display_name=KNOWLEDGE_BASE_NAME)
    response = client.create_knowledge_base(project_path, knowledge_base)
    knowledge_base_id = response.name.split(
        '/knowledgeBases/')[1].split('\n')[0]

    yield

    # Delete the created knowledge base
    knowledge_base_path = client.knowledge_base_path(
        PROJECT_ID, knowledge_base_id)
    client.delete_knowledge_base(knowledge_base_path)


def test_list_knowledge_base(capsys):
    knowledge_base_management.list_knowledge_bases(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert KNOWLEDGE_BASE_NAME in out
