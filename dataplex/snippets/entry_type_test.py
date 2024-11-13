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

import create_entry_type
import delete_entry_type
import get_entry_type
import list_entry_types
import update_entry_type

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"
ENTRY_TYPE_ID = f"test-entry-type-{str(uuid.uuid4()).split('-')[0]}"
EXPECTED_ENTRY_TYPE = (
    f"projects/{PROJECT_ID}/locations/{LOCATION}/entryTypes/{ENTRY_TYPE_ID}"
)


@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown_entry_type() -> None:
    try:
        # Create Entry Type resource that will be used in tests for "get", "list" and "update" methods
        create_entry_type.create_entry_type(PROJECT_ID, LOCATION, ENTRY_TYPE_ID)
        yield
    finally:
        # Clean-up Entry Type resource created above
        delete_entry_type.delete_entry_type(PROJECT_ID, LOCATION, ENTRY_TYPE_ID)


@Retry()
def test_list_entry_types() -> None:
    entry_types = list_entry_types.list_entry_types(PROJECT_ID, LOCATION)
    assert EXPECTED_ENTRY_TYPE in [entry_type.name for entry_type in entry_types]


@Retry()
def test_get_entry_type() -> None:
    entry_type = get_entry_type.get_entry_type(PROJECT_ID, LOCATION, ENTRY_TYPE_ID)
    assert EXPECTED_ENTRY_TYPE == entry_type.name


@Retry()
def test_update_entry_type() -> None:
    entry_type = update_entry_type.update_entry_type(
        PROJECT_ID, LOCATION, ENTRY_TYPE_ID
    )
    assert EXPECTED_ENTRY_TYPE == entry_type.name


@Retry()
def test_create_entry_type() -> None:
    entry_type_id_to_create = f"test-entry-type-{str(uuid.uuid4()).split('-')[0]}"
    expected_entry_type_to_create = f"projects/{PROJECT_ID}/locations/{LOCATION}/entryTypes/{entry_type_id_to_create}"
    try:
        entry_type = create_entry_type.create_entry_type(
            PROJECT_ID, LOCATION, entry_type_id_to_create
        )
        assert expected_entry_type_to_create == entry_type.name
    finally:
        # Clean-up created Entry Type
        delete_entry_type.delete_entry_type(
            PROJECT_ID, LOCATION, entry_type_id_to_create
        )


@Retry()
def test_delete_entry_type() -> None:
    entry_type_id_to_delete = f"test-entry-type-{str(uuid.uuid4()).split('-')[0]}"
    # Create Entry Type to be deleted
    create_entry_type.create_entry_type(PROJECT_ID, LOCATION, entry_type_id_to_delete)
    # No exception means successful call
    delete_entry_type.delete_entry_type(PROJECT_ID, LOCATION, entry_type_id_to_delete)
