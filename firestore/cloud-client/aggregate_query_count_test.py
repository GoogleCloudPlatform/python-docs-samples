# Copyright 2023 Google LLC
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

from aggregate_query_count import create_count_query


os.environ["GOOGLE_CLOUD_PROJECT"] = os.environ["FIRESTORE_PROJECT"]
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_create_count_query(capsys):
    create_count_query(project_id=PROJECT_ID)
    out, _ = capsys.readouterr()

    assert "Alias of results from query: all" in out
    assert "Number of" in out
