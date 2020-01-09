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
import pytest

import dialogflow_v2 as dialogflow

import context_management

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
SESSION_ID = 'session_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
CONTEXT_ID = 'context_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")


@pytest.fixture(scope="function", autouse=True)
def teardown():
    yield

    # Delete the created context
    contexts_client = dialogflow.ContextsClient()
    context_name = contexts_client.context_path(
        PROJECT_ID, SESSION_ID, CONTEXT_ID)
    contexts_client.delete_context(context_name)


def test_create_context(capsys):
    context_management.create_context(PROJECT_ID, SESSION_ID, CONTEXT_ID, 0)

    out, _ = capsys.readouterr()
    assert CONTEXT_ID in out
