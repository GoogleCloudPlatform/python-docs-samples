# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

import hello


@pytest.fixture
def client():
    hello.app.testing = True
    return hello.app.test_client()


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.text.startswith("Hello. This page was last updated at ")
    assert response.text.endswith("3:01 PM PST, Friday, January 8, 2024.")


def test_other_page(client):
    response = client.get("/help")
    assert response.status_code == 404
