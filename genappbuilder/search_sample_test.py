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

import search_sample

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "global"
search_engine_id = "test-search-engine"
serving_config_id = "default_config"
search_query = "Google"


def test_search(capsys):
    search_sample.search_sample(
        project_id=project_id,
        location=location,
        search_engine_id=search_engine_id,
        serving_config_id=serving_config_id,
        search_query=search_query,
    )

    out, _ = capsys.readouterr()

    assert search_query in out
