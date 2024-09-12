# Copyright 2024 Google LLC
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
# TODO: Delete this file after aproving /extensions folder

import os

from typing import Generator

import pytest

import gemini_extensions

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "us-central1"


@pytest.fixture(scope="module")
def extension_id() -> Generator[str, None, None]:
    extension = gemini_extensions.create_extension()
    yield extension.resource_name
    print("Deleting Extension...")
    gemini_extensions.delete_extension(extension.resource_name)


def test_create_extension_basic(extension_id: str) -> None:
    assert extension_id


def test_execute_extension(extension_id: str) -> None:
    response = gemini_extensions.execute_extension(extension_id)
    assert response


def test_get_extension(extension_id: str) -> None:
    response = gemini_extensions.get_extension(extension_id)
    assert response


def test_list_extensions() -> None:
    response = gemini_extensions.list_extensions()
    assert response
