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
import sys
from typing import Generator

import pytest

import gemini_reasoning_engine

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "us-central1"
STAGING_BUCKET = "gs://ucaip-samples-us-central1/reasoning_engine"


@pytest.mark.skipif(sys.version_info >= (3, 12), reason="Python 3.12 is not supported")
@pytest.fixture(scope="module")
def reasoning_engine_id() -> Generator[str, None, None]:
    reasoning_engine = gemini_reasoning_engine.create_reasoning_engine_basic(
        PROJECT_ID, STAGING_BUCKET
    )
    yield reasoning_engine.resource_name
    print("Deleting Reasoning Engine...")
    gemini_reasoning_engine.delete_reasoning_engine(
        PROJECT_ID, reasoning_engine.resource_name
    )


def test_create_reasoning_engine_basic(reasoning_engine_id: str) -> None:
    assert reasoning_engine_id


def test_create_reasoning_engine_advanced() -> None:
    reasoning_engine = gemini_reasoning_engine.create_reasoning_engine_advanced(
        PROJECT_ID, REGION, STAGING_BUCKET
    )
    assert reasoning_engine
    gemini_reasoning_engine.delete_reasoning_engine(
        PROJECT_ID, reasoning_engine.resource_name
    )


def test_query_reasoning_engine(reasoning_engine_id: str) -> None:
    response = gemini_reasoning_engine.query_reasoning_engine(
        PROJECT_ID, reasoning_engine_id
    )
    assert response


def test_list_reasoning_engines() -> None:
    response = gemini_reasoning_engine.list_reasoning_engines(PROJECT_ID)
    assert response


def test_get_reasoning_engine(reasoning_engine_id: str) -> None:
    response = gemini_reasoning_engine.get_reasoning_engine(
        PROJECT_ID, reasoning_engine_id
    )
    assert response
