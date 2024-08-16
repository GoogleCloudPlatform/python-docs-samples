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
import os

import backoff
from google.api_core.exceptions import ResourceExhausted

import anthropic_claude_3_tool_use


_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_tool_use() -> None:
    response = anthropic_claude_3_tool_use.tool_use(_PROJECT_ID)
    json_response = response.model_dump_json(indent=2)
    assert "restaurant" in json_response
    assert "tool_use" in json_response
    assert "text_search_places_api" in json_response
