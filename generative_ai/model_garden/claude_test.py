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

import claude_3_streaming_example
import claude_3_tool_example
import claude_3_unary_example


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_generate_text_streaming() -> None:
    responses = claude_3_streaming_example.generate_text_streaming()
    assert "bread" in responses


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_tool_use() -> None:
    response = claude_3_tool_example.tool_use()
    json_response = response.model_dump_json(indent=2)
    assert "restaurant" in json_response
    assert "tool_use" in json_response
    assert "text_search_places_api" in json_response


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_generate_text() -> None:
    responses = claude_3_unary_example.generate_text()
    assert "bread" in responses.model_dump_json(indent=2)
