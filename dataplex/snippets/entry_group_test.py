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

import create_entry_group
import delete_entry_group
import get_entry_group
import list_entry_groups
import update_entry_group

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"
ENTRY_GROUP_ID = f"test-entry-group-{str(uuid.uuid4()).split('-')[0]}"
EXPECTED_ENTRY_GROUP = (
    f"projects/{PROJECT_ID}/locations/{LOCATION}/entryGroups/{ENTRY_GROUP_ID}"
)


@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown_entry_group() -> None:
    try:
        # Create Entry Group resource that will be used in tests for "get", "list" and "update" methods
        create_entry_group.create_entry_group(PROJECT_ID, LOCATION, ENTRY_GROUP_ID)
        yield
    finally:
        # Clean-up Entry Group resource created above
        delete_entry_group.delete_entry_group(PROJECT_ID, LOCATION, ENTRY_GROUP_ID)


@Retry()
def test_list_entry_groups() -> None:
    entry_groups = list_entry_groups.list_entry_groups(PROJECT_ID, LOCATION)
    assert EXPECTED_ENTRY_GROUP in [entry_group.name for entry_group in entry_groups]


@Retry()
def test_get_entry_group() -> None:
    entry_group = get_entry_group.get_entry_group(PROJECT_ID, LOCATION, ENTRY_GROUP_ID)
    assert EXPECTED_ENTRY_GROUP == entry_group.name


@Retry()
def test_update_entry_group() -> None:
    entry_group = update_entry_group.update_entry_group(
        PROJECT_ID, LOCATION, ENTRY_GROUP_ID
    )
    assert EXPECTED_ENTRY_GROUP == entry_group.name


@Retry()
def test_create_entry_group() -> None:
    entry_group_id_to_create = f"test-entry-group-{str(uuid.uuid4()).split('-')[0]}"
    expected_entry_group_to_create = f"projects/{PROJECT_ID}/locations/{LOCATION}/entryGroups/{entry_group_id_to_create}"
    try:
        entry_group = create_entry_group.create_entry_group(
            PROJECT_ID, LOCATION, entry_group_id_to_create
        )
        assert expected_entry_group_to_create == entry_group.name
    finally:
        # Clean-up created Entry Group
        delete_entry_group.delete_entry_group(
            PROJECT_ID, LOCATION, entry_group_id_to_create
        )


@Retry()
def test_delete_entry_group() -> None:
    entry_group_id_to_delete = f"test-entry-group-{str(uuid.uuid4()).split('-')[0]}"
    # Create Entry Group to be deleted
    create_entry_group.create_entry_group(
        PROJECT_ID, LOCATION, entry_group_id_to_delete
    )
    # No exception means successful call
    delete_entry_group.delete_entry_group(
        PROJECT_ID, LOCATION, entry_group_id_to_delete
    )
