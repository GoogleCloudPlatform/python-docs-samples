# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import backoff

from google.api_core.exceptions import ResourceExhausted

import text_example01
import text_example02
import text_example03
import text_stream_example01
import text_stream_example02


def test_non_stream_text_basic() -> None:
    response = text_example03.generate_content()
    assert response


def test_gemini_text_input_example() -> None:
    text = text_example01.generate_from_text_input()
    assert len(text) > 0


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_interview() -> None:
    content = text_example02.interview()
    # check if response is empty
    assert len(content) > 0


def test_stream_text_basic() -> None:
    responses = text_stream_example01.generate_content()
    assert responses


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_streaming_prediction() -> None:
    responses = text_stream_example02.streaming_prediction()
    print(responses)
    assert "1." in responses
    assert "?" in responses
    assert "you" in responses
    assert "do" in responses
