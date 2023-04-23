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

from detect_intent_synthesize_tts_response import detect_intent_synthesize_tts_response


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
AGENT_ID = os.getenv("AGENT_ID")


def test_detect_intent_positive(capsys, tmp_path_factory):

    output_file = tmp_path_factory.mktemp("data") / "tmp.wav"

    detect_intent_synthesize_tts_response(
        PROJECT_ID,
        "global",
        AGENT_ID,
        "Perfect!",
        "OUTPUT_AUDIO_ENCODING_LINEAR_16",
        "en-us",
        output_file,
    )
    out, _ = capsys.readouterr()
    assert f"Audio content written to file: {output_file}" in out
