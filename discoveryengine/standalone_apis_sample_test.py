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

from discoveryengine import standalone_apis_sample

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_check_grounding():
    response = standalone_apis_sample.check_grounding_sample(project_id)
    assert response
    assert response.support_score
    assert response.cited_chunks
    assert response.claims


def test_rank():
    response = standalone_apis_sample.rank_sample(project_id)
    assert response
    assert response.records
