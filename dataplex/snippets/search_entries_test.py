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
import os
import time

import uuid

from google.api_core.retry import Retry

import pytest

import create_entry
import create_entry_group
import delete_entry_group
import search_entries

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"
ID = str(uuid.uuid4()).split("-")[0]
ENTRY_GROUP_ID = f"test-entry-group-{ID}"
ENTRY_ID = f"test-entry-{ID}"
EXPECTED_ENTRY = f"/{LOCATION}/entryGroups/{ENTRY_GROUP_ID}/entries/{ENTRY_ID}"


@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown_entry_group() -> None:
    try:
        create_entry_group.create_entry_group(PROJECT_ID, LOCATION, ENTRY_GROUP_ID)
        create_entry.create_entry(PROJECT_ID, LOCATION, ENTRY_GROUP_ID, ENTRY_ID)
        time.sleep(30)
        yield
    finally:
        # Entry inside this Entry Group will be deleted automatically
        delete_entry_group.delete_entry_group(PROJECT_ID, LOCATION, ENTRY_GROUP_ID)


@Retry()
def test_search_entries() -> None:
    query = "name:test-entry- AND description:description AND aspect:generic"
    entries = search_entries.search_entries(PROJECT_ID, query)
    assert EXPECTED_ENTRY in [entry.name.split("locations")[1] for entry in entries]
