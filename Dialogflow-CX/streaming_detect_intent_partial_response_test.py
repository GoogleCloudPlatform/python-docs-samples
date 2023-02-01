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

"""Tests for detect_intent_texts."""

from __future__ import absolute_import

import os

from streaming_detect_intent_partial_response import (
    streaming_detect_intent_partial_response,
)


DIRNAME = os.path.realpath(os.path.dirname(__file__))
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
AGENT_ID = os.getenv("AGENT_ID")
AUDIO_PATH = os.getenv("AUDIO_PATH")
AUDIO = f"{DIRNAME}/{AUDIO_PATH}"


def test_streaming_detect_intent_partial_response(capsys):

    encoding = "AUDIO_ENCODING_LINEAR_16"
    sample_rate_hertz = 24000

    streaming_detect_intent_partial_response(
        PROJECT_ID,
        "global",
        AGENT_ID,
        AUDIO,
        encoding,
        sample_rate_hertz,
        "en-US",
    )
    out, _ = capsys.readouterr()

    assert "Intermediate transcript:" in out
    assert "Response text: Hi! I'm the virtual flights agent." in out
