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

"""Tests for detect_intent_texts."""


import os
import uuid


from detect_intent_texts import detect_intent_texts

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
AGENT_ID = os.getenv("AGENT_ID")
AGENT = f"projects/{PROJECT_ID}/locations/global/agents/{AGENT_ID}"
SESSION_ID = uuid.uuid4()
TEXTS = ["hello", "book a flight"]
AGENT_ID_US_CENTRAL1 = os.getenv("AGENT_ID_US_CENTRAL1")
AGENT_US_CENTRAL1 = (
    f"projects/{PROJECT_ID}/locations/us-central1/agents/{AGENT_ID_US_CENTRAL1}"
)


def test_detect_intent_texts(capsys):
    detect_intent_texts(AGENT, SESSION_ID, TEXTS, "en-US")
    out, _ = capsys.readouterr()

    assert "Response text: I can help you find a ticket" in out


def test_detect_intent_texts_regional(capsys):
    detect_intent_texts(AGENT_US_CENTRAL1, SESSION_ID, TEXTS, "en-US")
    out, _ = capsys.readouterr()

    assert "Response text: I can help you find a ticket" in out
