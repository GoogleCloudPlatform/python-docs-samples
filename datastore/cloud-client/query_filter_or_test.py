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

from google.cloud import datastore
import pytest

from query_filter_or import query_filter_or

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture()
def entities():
    client = datastore.Client(project=PROJECT_ID)

    entities = []
    for description in ["Buy milk", "Feed cats", "Walk dog"]:
        task_key = client.key("Task")
        task_obj = datastore.Entity(key=task_key)
        task_obj["description"] = description
        client.put(task_obj)
        entities.append(task_obj)

    yield entities

    # delete all Tasks
    for task in client.query(kind="Task").fetch():
        client.delete(task)


def test_query_filter_or(capsys, entities):
    results = query_filter_or(project_id=PROJECT_ID)
    descriptions = [result.popitem()[1] for result in results]
    assert "Feed cats" in descriptions
    assert "Buy milk" in descriptions
    assert "Walk dog" not in descriptions
