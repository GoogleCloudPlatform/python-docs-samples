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

    task_key = client.key("Task")
    task1 = datastore.Entity(key=task_key)
    task1["description"] = "Buy milk"
    client.put(task1)

    task_key2 = client.key("Task")
    task2 = datastore.Entity(key=task_key2)
    task2["description"] = "Feed cats"
    client.put(task2)

    yield entities

    client.delete(task1)
    client.delete(task2)


def test_query_filter_or(capsys, entities):
    query_filter_or(project_id=PROJECT_ID)
    out, _ = capsys.readouterr()
    assert "Feed cats" in out
