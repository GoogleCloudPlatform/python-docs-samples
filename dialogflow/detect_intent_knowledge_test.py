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

import detect_intent_knowledge

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
SESSION_ID = "session_{}".format(uuid.uuid4())
KNOWLEDGE_BASE_ID = "MjEwMjE4MDQ3MDQwMDc0NTQ3Mg"
TEXTS = ["Where is my data stored?"]


def test_detect_intent_knowledge(capsys):
    detect_intent_knowledge.detect_intent_knowledge(
        PROJECT_ID, SESSION_ID, "en-us", KNOWLEDGE_BASE_ID, TEXTS
    )

    out, _ = capsys.readouterr()
    assert "Knowledge results" in out
