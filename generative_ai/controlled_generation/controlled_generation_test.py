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

import example_01
import example_02
import example_03
import example_04
import example_05
import example_06
import example_07

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def test_config_response_mime_type() -> None:
    response = example_05.generate_content()
    assert response


def test_config_response_schema() -> None:
    response = example_01.generate_content()
    assert response


def test_config_response_schema2() -> None:
    response = example_02.generate_content()
    assert response


def test_config_response_schema3() -> None:
    response = example_03.generate_content()
    assert response


def test_config_response_schema4() -> None:
    response = example_04.generate_content()
    assert response


def test_config_response_schema6() -> None:
    response = example_06.generate_content()
    assert response


def test_config_response_schema7() -> None:
    response = example_07.generate_content()
    assert response
