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

import create_aspect_type
import delete_aspect_type
import get_aspect_type
import list_aspect_types
import update_aspect_type

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"
ASPECT_TYPE_ID = f"test-aspect-type-{str(uuid.uuid4()).split('-')[0]}"
EXPECTED_ASPECT_TYPE = (
    f"projects/{PROJECT_ID}/locations/{LOCATION}/aspectTypes/{ASPECT_TYPE_ID}"
)


@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown_aspect_type() -> None:
    try:
        # Create Aspect Type resource that will be used in tests for "get", "list" and "update" methods
        create_aspect_type.create_aspect_type(PROJECT_ID, LOCATION, ASPECT_TYPE_ID, [])
        yield
    finally:
        # Clean-up Aspect Type resource created above
        delete_aspect_type.delete_aspect_type(PROJECT_ID, LOCATION, ASPECT_TYPE_ID)


@Retry()
def test_list_aspect_types() -> None:
    aspect_types = list_aspect_types.list_aspect_types(PROJECT_ID, LOCATION)
    assert EXPECTED_ASPECT_TYPE in [aspect_type.name for aspect_type in aspect_types]


@Retry()
def test_get_aspect_type() -> None:
    aspect_type = get_aspect_type.get_aspect_type(PROJECT_ID, LOCATION, ASPECT_TYPE_ID)
    assert EXPECTED_ASPECT_TYPE == aspect_type.name


@Retry()
def test_update_aspect_type() -> None:
    aspect_type = update_aspect_type.update_aspect_type(
        PROJECT_ID, LOCATION, ASPECT_TYPE_ID, []
    )
    assert EXPECTED_ASPECT_TYPE == aspect_type.name


@Retry()
def test_create_aspect_type() -> None:
    aspect_type_id_to_create = f"test-aspect-type-{str(uuid.uuid4()).split('-')[0]}"
    expected_aspect_type_to_create = f"projects/{PROJECT_ID}/locations/{LOCATION}/aspectTypes/{aspect_type_id_to_create}"
    try:
        aspect_type = create_aspect_type.create_aspect_type(
            PROJECT_ID, LOCATION, aspect_type_id_to_create, []
        )
        assert expected_aspect_type_to_create == aspect_type.name
    finally:
        # Clean-up created Aspect Type
        delete_aspect_type.delete_aspect_type(
            PROJECT_ID, LOCATION, aspect_type_id_to_create
        )


@Retry()
def test_delete_aspect_type() -> None:
    aspect_type_id_to_delete = f"test-aspect-type-{str(uuid.uuid4()).split('-')[0]}"
    # Create Aspect Type to be deleted
    create_aspect_type.create_aspect_type(
        PROJECT_ID, LOCATION, aspect_type_id_to_delete, []
    )
    # No exception means successful call
    delete_aspect_type.delete_aspect_type(
        PROJECT_ID, LOCATION, aspect_type_id_to_delete
    )
