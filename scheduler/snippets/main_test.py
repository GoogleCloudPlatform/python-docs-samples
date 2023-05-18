# Copyright 2019 Google LLC
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

from flask.testing import FlaskClient
import pytest


@pytest.fixture
def app() -> FlaskClient:
    import main

    main.app.testing = True
    return main.app.test_client()


def test_index(app: FlaskClient) -> None:
    r = app.get("/")
    assert r.status_code == 200


def test_log_payload(app: FlaskClient) -> None:
    payload = "test_payload"
    response = app.post("/log_payload", data=payload)
    assert response.status_code == 200
    assert payload in response.text


def test_empty_payload(app: FlaskClient) -> None:
    response = app.post("/log_payload")
    assert response.status_code == 200
    assert "empty payload" in response.text
