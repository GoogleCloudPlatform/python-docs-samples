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
import local_sdk_example
import multimodal_token_count_example
import simple_example


def test_count_token() -> None:
    assert local_sdk_example.count_token_locally()
    assert api_example.count_token_service()


def test_gemini_count_token_example() -> None:
    response = simple_example.count_tokens()
    assert response
    assert response.usage_metadata

    response = multimodal_token_count_example.count_tokens_multimodal()
    assert response
    assert response.usage_metadata
