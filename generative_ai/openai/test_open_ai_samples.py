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

import chat_openai_example
import chat_openai_image_example
import chat_openai_image_stream_example
import chat_openai_stream_example
import credentials_refresher_usage_example


def test_credentials_refresher() -> None:
    response = credentials_refresher_usage_example.generate_text()
    assert response


def test_non_streaming_text() -> None:
    response = chat_openai_example.generate_text()
    assert response


def test_non_streaming_image() -> None:
    response = chat_openai_image_example.generate_text()
    assert response


def test_streaming_image() -> None:
    response = chat_openai_image_stream_example.generate_text()
    assert response


def test_streaming_text() -> None:
    response = chat_openai_stream_example.generate_text()
    assert response
