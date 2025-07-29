# Copyright 2025 Google LLC
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

import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture
def client():
    return TestClient(main.app)


def test_handler_no_param(client):
    r = client.get("/")

    assert r.json() == {"message": "Hello World!"}
    assert r.status_code == 200


def test_handler_with_param(client):
    r = client.get("/", params={"name": "Foo"})

    assert r.json() == {"message": "Hello Foo!"}
    assert r.status_code == 200
