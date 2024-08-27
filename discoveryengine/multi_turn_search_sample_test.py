# Copyright 2023 Google LLC
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

from discoveryengine import multi_turn_search_sample

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
search_queries = ["What is Google?", "What was their revenue in 2021?"]


def test_multi_turn_search():
    location = "global"
    data_store_id = "alphabet-earnings-reports_1697472013405"
    responses = multi_turn_search_sample.multi_turn_search_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        search_queries=search_queries,
    )

    assert responses

    for response in responses:
        assert response.reply
        assert response.conversation
        assert response.search_results

        for result in response.search_results:
            assert result.document.name
