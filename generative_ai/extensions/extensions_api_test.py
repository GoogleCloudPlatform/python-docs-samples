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

import execute_extension
import extension_basic
import get_extension
import list_extension

EXTENSION_ID = "EXTENSION_ID"
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "us-central1"


def test_execute_extension() -> None:
    response = execute_extension.generate_content(
        PROJECT_ID, REGION, EXTENSION_ID)
    assert response


def test_extension_basic() -> None:
    response = extension_basic.generate_content(PROJECT_ID, REGION)
    assert response


def test_get_extension() -> None:
    response = get_extension.generate_content(PROJECT_ID, REGION, EXTENSION_ID)
    assert response


def test_list_extension() -> None:
    response = list_extension.generate_content(PROJECT_ID, REGION)
    assert response
