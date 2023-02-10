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

"""Tests for detect_intent_with_sentiment_analysis.py"""

from __future__ import absolute_import

import os

from detect_intent_with_intent_input import detect_intent_with_intent_input


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
AGENT_ID = os.getenv("AGENT_ID")
INTENT_ID = os.getenv("INTENT_ID")


def test_detect_intent_with_intent_input():
    response_text = detect_intent_with_intent_input(
        PROJECT_ID,
        "global",
        AGENT_ID,
        INTENT_ID,
        "en-us",
    )
    assert len(response_text) == 2
    assert response_text[0] == ["Let's find a one-way ticket for you. "]
    assert response_text[1] == ["Which city are you leaving from?"]
