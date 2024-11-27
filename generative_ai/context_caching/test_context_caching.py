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

from typing import Generator

import pytest

import create_context_cache
import delete_context_cache
import get_context_cache
import list_context_caches
import update_context_cache
import use_context_cache

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "us-central1"


@pytest.fixture(scope="module")
def cache_id() -> Generator[str, None, None]:
    cached_content_name = create_context_cache.create_context_cache()
    yield cached_content_name
    delete_context_cache.delete_context_cache(cached_content_name)


def test_create_context_cache(cache_id: str) -> None:
    assert cache_id


def test_use_context_cache(cache_id: str) -> None:
    response = use_context_cache.use_context_cache(cache_id)
    assert response


def test_get_context_cache(cache_id: str) -> None:
    response = get_context_cache.get_context_cache(cache_id)
    assert response


def test_get_list_of_context_caches(cache_id: str) -> None:
    response = list_context_caches.list_context_caches()
    assert cache_id in response


def test_update_context_cache(cache_id: str) -> None:
    response = update_context_cache.update_context_cache(cache_id)
    assert response
