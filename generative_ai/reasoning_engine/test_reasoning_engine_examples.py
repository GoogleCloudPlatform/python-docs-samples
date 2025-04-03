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

from typing import Generator

import pytest

import create_reasoning_engine_advanced_example
import create_reasoning_engine_example
import delete_reasoning_engine_example
import get_reasoning_engine_example
import list_reasoning_engine_example
import query_reasoning_engine_example


STAGING_BUCKET = "gs://ucaip-samples-us-central1"


@pytest.fixture(scope="module")
def reasoning_engine_id() -> Generator[str, None, None]:
    reasoning_engine = create_reasoning_engine_example.create_reasoning_engine_basic(
        STAGING_BUCKET
    )
    yield reasoning_engine.resource_name
    print("Deleting Reasoning Engine...")
    delete_reasoning_engine_example.delete_reasoning_engine(
        reasoning_engine.resource_name
    )


@pytest.mark.skip("TODO: Reasoning Engine Deployment Issue b/339643184")
def test_create_reasoning_engine_basic(reasoning_engine_id: str) -> None:
    assert reasoning_engine_id


@pytest.mark.skip("TODO: Reasoning Engine Deployment Issue b/339643184")
def test_create_reasoning_engine_advanced() -> None:
    reasoning_engine = (
        create_reasoning_engine_advanced_example.create_reasoning_engine_advanced(
            STAGING_BUCKET
        )
    )
    assert reasoning_engine
    delete_reasoning_engine_example.delete_reasoning_engine(
        reasoning_engine.resource_name
    )


@pytest.mark.skip("TODO: Resolve issue b/348193408")
def test_query_reasoning_engine(reasoning_engine_id: str) -> None:
    response = query_reasoning_engine_example.query_reasoning_engine(
        reasoning_engine_id
    )
    assert response
    assert response == "1 + 2 is 3"


def test_list_reasoning_engines() -> None:
    response = list_reasoning_engine_example.list_reasoning_engines()
    assert response


@pytest.mark.skip("TODO: Resolve issue b/348193408")
def test_get_reasoning_engine(reasoning_engine_id: str) -> None:
    response = get_reasoning_engine_example.get_reasoning_engine(reasoning_engine_id)
    assert response
