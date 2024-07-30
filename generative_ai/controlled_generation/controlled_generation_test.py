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

import response_mime_type
import response_schema


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_config_response_mime_type() -> None:
    response = response_mime_type.generate_content(PROJECT_ID)
    assert response


def test_config_response_schema() -> None:
    response = response_schema.generate_content(PROJECT_ID)
    assert response


def test_config_response_schema2() -> None:
    response = response_schema.generate_content2(PROJECT_ID)
    assert response


def test_config_response_schema3() -> None:
    response = response_schema.generate_content3(PROJECT_ID)
    assert response


def test_config_response_schema4() -> None:
    response = response_schema.generate_content4(PROJECT_ID)
    assert response


def test_config_response_schema6() -> None:
    response = response_schema.generate_content6(PROJECT_ID)
    assert response
