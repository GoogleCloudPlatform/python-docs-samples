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


import os

import pytest

import delete_extension
import execute_extension
import extension_basic
import get_extension
import list_extension

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "us-central1"


@pytest.fixture(scope="module")
def extension_id():
    response = extension_basic.generate_content(PROJECT_ID)
    extension_id_part = response.split('extensions/')[-1].split('/')[0]
    extension_id = ''.join(filter(str.isdigit, extension_id_part))
    print("Extension_id", extension_id)
    yield extension_id
    print("Deleting Extension...")
    delete_response = delete_extension.generate_content(
        PROJECT_ID, extension_id)
    assert delete_response


def test_extension_basic(extension_id) -> None:
    assert extension_id


def test_execute_extension(extension_id) -> None:
    response = execute_extension.generate_content(
        PROJECT_ID, extension_id)
    assert response


def test_get_extension(extension_id) -> None:
    response = get_extension.generate_content(PROJECT_ID, extension_id)
    assert response


def test_list_extension() -> None:
    response = list_extension.generate_content(PROJECT_ID)
    assert response

