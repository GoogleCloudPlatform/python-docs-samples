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


def test_local_sdk_example() -> None:
    assert local_sdk_example.local_tokenizer_example()
    assert api_example.count_token_api_example()


def test_simple_example() -> None:
    response = simple_example.count_token_example()
    assert response
    assert response.usage_metadata


def test_multimodal_example() -> None:
    print(dir(multimodal_token_count_example))
    response = multimodal_token_count_example.count_tokens_multimodal_example()
    assert response
    assert response.usage_metadata
