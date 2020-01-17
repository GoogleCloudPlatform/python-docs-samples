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

import document_management

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
DOCUMENT_DISPLAY_NAME = 'DO_NOT_DELETE_TEST_DOCUMENT'
KNOWLEDGE_BASE_ID = 'MjEwMjE4MDQ3MDQwMDc0NTQ3Mg'


def test_list_documents(capsys):
    document_management.list_documents(PROJECT_ID, KNOWLEDGE_BASE_ID)
    out, _ = capsys.readouterr()
    assert DOCUMENT_DISPLAY_NAME in out
