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

import api_example
import count_token_example
import list_tokens_example
import local_sdk_example
import multimodal_example
import simple_example


def test_count_token_sdk_example() -> None:
    assert local_sdk_example.count_token_sdk_example()
    assert count_token_example.count_token_sdk_example()


def test_count_token_api_example() -> None:
    assert api_example.count_token_api_example()
    assert count_token_example.count_token_api_example()


def test_gemini_count_simple_example() -> None:
    response = simple_example.count_tokens_example()
    assert response
    assert response.usage_metadata


def test_gemini_count_tokens_multimodal_example() -> None:
    response = multimodal_example.count_tokens_multimodal_example()
    assert response
    assert response.usage_metadata


def test_compute_tokens_example() -> None:
    assert list_tokens_example.list_tokens_example()
