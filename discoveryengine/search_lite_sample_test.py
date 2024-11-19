# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

from discoveryengine import search_lite_sample

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
api_key = os.environ["VERTEX_AI_SEARCH_API_KEY"]
search_query = "Google"


def test_search_lite():
    location = "global"
    engine_id = "test-search-engine_1689960780551"
    response = search_lite_sample.search_lite_sample(
        project_id=project_id,
        location=location,
        engine_id=engine_id,
        api_key=api_key,
        search_query=search_query,
    )

    assert response
    assert response.results

    for result in response.results:
        assert result.document.name
        break
