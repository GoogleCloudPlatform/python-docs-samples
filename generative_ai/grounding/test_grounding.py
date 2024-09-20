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

import palm_example
import vais_example
import web_example


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_grounding() -> None:
    data_store_id = "test-search-engine_1689960780551"
    response = palm_example.grounding(
        data_store_location="global",
        data_store_id=data_store_id,
    )
    assert response
    assert response.text
    assert response.grounding_metadata


def test_gemini_grounding_vais_example() -> None:
    response = vais_example.generate_text_with_grounding_vertex_ai_search(
        "grounding-test-datastore"
    )
    assert response


def test_gemini_grounding_web_example() -> None:
    response = web_example.generate_text_with_grounding_web()
    assert response
