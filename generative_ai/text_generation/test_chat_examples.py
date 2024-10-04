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

import chat_code_example
import chat_example
import chat_multiturn_example
import chat_multiturn_stream_example
import chat_openai_example
import chat_openai_image_example
import chat_openai_image_stream_example
import chat_openai_stream_example

from google.api_core.exceptions import ResourceExhausted


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_chat_example() -> None:
    assert len(chat_example.send_chat()) > 0


def test_gemini_chat_example() -> None:
    text = chat_multiturn_example.chat_text_example()
    text = text.lower()
    assert len(text) > 0
    assert any([_ in text for _ in ("hi", "hello", "greeting")])

    text = chat_multiturn_stream_example.chat_stream_example()
    text = text.lower()
    assert len(text) > 0
    assert any([_ in text for _ in ("hi", "hello", "greeting")])


def test_non_streaming_image() -> None:
    response = chat_openai_image_example.generate_text()
    assert response


def test_non_streaming_text() -> None:
    response = chat_openai_example.generate_text()
    assert response


def test_streaming_image() -> None:
    response = chat_openai_image_stream_example.generate_text()
    assert response


def test_streaming_text() -> None:
    response = chat_openai_stream_example.generate_text()
    assert response


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_code_chat() -> None:
    content = chat_code_example.write_a_function().text
    assert len(content) > 0
