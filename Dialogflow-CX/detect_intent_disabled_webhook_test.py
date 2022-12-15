# Copyright 2022, Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for detect_intent_with_sentiment_analysis.py"""

from __future__ import absolute_import

import os

from detect_intent_disabled_webhook import detect_intent_disabled_webhook


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
AGENT_ID = os.getenv("AGENT_ID")


def test_detect_intent_positive():
    response_text_list = detect_intent_disabled_webhook(
        PROJECT_ID,
        "global",
        AGENT_ID,
        "Perfect!",
        "en-us",
    )
    for response_text in response_text_list:
        assert response_text[0] in [
            "You are welcome!",
            "It's my pleasure.",
            "Anytime.",
            "Of course.",
            "It's my pleasure to serve you.",
        ]
