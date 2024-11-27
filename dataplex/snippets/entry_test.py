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

import uuid

from google.api_core.retry import Retry

import pytest

import create_entry
import create_entry_group
import delete_entry
import delete_entry_group
import get_entry
import list_entries
import lookup_entry
import update_entry

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"
ID = str(uuid.uuid4()).split("-")[0]
ENTRY_GROUP_ID = f"test-entry-group-{ID}"
ENTRY_ID = f"test-entry-{ID}"
EXPECTED_ENTRY = f"projects/{PROJECT_ID}/locations/{LOCATION}/entryGroups/{ENTRY_GROUP_ID}/entries/{ENTRY_ID}"


@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown_entry_group() -> None:
    try:
        # Create Entry Group resource that will be used for creating Entry
        create_entry_group.create_entry_group(PROJECT_ID, LOCATION, ENTRY_GROUP_ID)
        # Create Entry that will be used in tests for "get", "lookup", "list" and "update" methods
        create_entry.create_entry(PROJECT_ID, LOCATION, ENTRY_GROUP_ID, ENTRY_ID)
        yield
    finally:
        # Clean-up Entry Group resource created above
        # Entry inside this Entry Group will be deleted automatically
        delete_entry_group.delete_entry_group(PROJECT_ID, LOCATION, ENTRY_GROUP_ID)


@Retry()
def test_list_entries() -> None:
    entries = list_entries.list_entries(PROJECT_ID, LOCATION, ENTRY_GROUP_ID)
    assert EXPECTED_ENTRY in [entry.name for entry in entries]


@Retry()
def test_get_entry() -> None:
    entry = get_entry.get_entry(PROJECT_ID, LOCATION, ENTRY_GROUP_ID, ENTRY_ID)
    assert EXPECTED_ENTRY == entry.name


@Retry()
def test_lookup_entry() -> None:
    entry = lookup_entry.lookup_entry(PROJECT_ID, LOCATION, ENTRY_GROUP_ID, ENTRY_ID)
    assert EXPECTED_ENTRY == entry.name


@Retry()
def test_update_entry() -> None:
    entry = update_entry.update_entry(PROJECT_ID, LOCATION, ENTRY_GROUP_ID, ENTRY_ID)
    assert EXPECTED_ENTRY in entry.name


@Retry()
def test_create_entry() -> None:
    entry_id_to_create = f"test-entry-{str(uuid.uuid4()).split('-')[0]}"
    expected_entry_to_create = f"projects/{PROJECT_ID}/locations/{LOCATION}/entryGroups/{ENTRY_GROUP_ID}/entries/{entry_id_to_create}"
    try:
        entry = create_entry.create_entry(
            PROJECT_ID, LOCATION, ENTRY_GROUP_ID, entry_id_to_create
        )
        assert expected_entry_to_create == entry.name
    finally:
        # Clean-up created Entry
        delete_entry.delete_entry(
            PROJECT_ID, LOCATION, ENTRY_GROUP_ID, entry_id_to_create
        )


@Retry()
def test_delete_entry() -> None:
    entry_id_to_delete = f"test-entry-{str(uuid.uuid4()).split('-')[0]}"
    # Create Entry to be deleted
    create_entry.create_entry(PROJECT_ID, LOCATION, ENTRY_GROUP_ID, entry_id_to_delete)
    # No exception means successful call
    delete_entry.delete_entry(PROJECT_ID, LOCATION, ENTRY_GROUP_ID, entry_id_to_delete)
