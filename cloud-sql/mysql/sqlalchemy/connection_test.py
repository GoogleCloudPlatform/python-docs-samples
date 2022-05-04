# Copyright 2018 Google LLC
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

import logging
import os

from flask.testing import FlaskClient

import pytest

import app

logger = logging.getLogger()


# load proper environment variables
def setup_test_env():
    os.environ["DB_USER"] = os.environ["MYSQL_USER"]
    os.environ["DB_PASS"] = os.environ["MYSQL_PASSWORD"]
    os.environ["DB_NAME"] = os.environ["MYSQL_DATABASE"]
    os.environ["DB_PORT"] = os.environ["MYSQL_PORT"]
    os.environ["INSTANCE_UNIX_SOCKET"] = os.environ["MYSQL_UNIX_SOCKET"]
    os.environ["INSTANCE_HOST"] = os.environ["MYSQL_INSTANCE_HOST"]
    os.environ["INSTANCE_CONNECTION_NAME"] = os.environ["MYSQL_INSTANCE"]


@pytest.fixture(scope="module")
def client() -> FlaskClient:
    setup_test_env()
    app.app.testing = True
    client = app.app.test_client()

    return client


def test_get_votes(client: FlaskClient) -> None:
    response = client.get("/")
    text = "Tabs VS Spaces"
    body = response.text
    assert response.status_code == 200
    assert text in body


def test_cast_vote(client: FlaskClient) -> None:
    response = client.post("/votes", data={"team": "SPACES"})
    text = "Vote successfully cast for 'SPACES'"
    body = response.text
    assert response.status_code == 200
    assert text in body


def test_unix_connection(client: FlaskClient) -> None:
    del os.environ["INSTANCE_HOST"]
    app.db = app.init_connection_pool()
    assert "unix_socket" in str(app.db.url)
    test_get_votes(client)
    test_cast_vote(client)


def test_connector_connection(client: FlaskClient) -> None:
    del os.environ["INSTANCE_UNIX_SOCKET"]
    app.db = app.init_connection_pool()
    assert str(app.db.url) == "mysql+pymysql://"
    test_get_votes(client)
    test_cast_vote(client)
