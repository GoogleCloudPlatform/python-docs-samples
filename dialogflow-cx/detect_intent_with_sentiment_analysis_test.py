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


import os

import pytest

from detect_intent_with_sentiment_analysis import detect_intent_with_sentiment_analysis


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
AGENT_ID = os.getenv("AGENT_ID")


@pytest.mark.parametrize(
    "text, expected_score_min, expected_score_max",
    (["Perfect", 0.5, 1], ["I am not happy", -1, -0.5]),
)
def test_detect_intent_positive(text, expected_score_min, expected_score_max):

    score = detect_intent_with_sentiment_analysis(
        PROJECT_ID,
        "global",
        AGENT_ID,
        text,
        "en-us",
    )
    assert expected_score_min < score < expected_score_max
