# Copyright 2020 Google LLC
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
from google.auth import default
import google.auth.transport.requests
import pytest
import requests

import app

logger = logging.getLogger()


CA_FILENAME = "certs/ca.pem"
SQLADMIN_API_ENDPOINT = "https://sqladmin.googleapis.com"
SQLADMIN_API_VERSION = "v1beta4"


# load proper environment variables
def setup_test_env():
    os.environ["DB_USER"] = os.environ["SQLSERVER_USER"]
    os.environ["DB_PASS"] = os.environ["SQLSERVER_PASSWORD"]
    os.environ["DB_NAME"] = os.environ["SQLSERVER_DATABASE"]
    os.environ["DB_PORT"] = os.environ["SQLSERVER_PORT"]
    os.environ["INSTANCE_HOST"] = os.environ["SQLSERVER_INSTANCE_HOST"]
    os.environ["INSTANCE_CONNECTION_NAME"] = os.environ["SQLSERVER_INSTANCE"]

    project, _, instance = os.environ["INSTANCE_CONNECTION_NAME"].split(":")
    download_ca_cert(project, instance)
    os.environ["DB_ROOT_CERT"] = CA_FILENAME


def download_ca_cert(project, instance):
    """ Download server CA cert"""
    scopes = ["https://www.googleapis.com/auth/sqlservice.admin"]
    credentials, _ = default(scopes=scopes)

    if not credentials.valid:
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)

    headers = {
        "Authorization": f"Bearer {credentials.token}",
    }
    url = (f"{SQLADMIN_API_ENDPOINT}/sql/{SQLADMIN_API_VERSION}"
           f"/projects/{project}/instances/{instance}/connectSettings")

    resp = requests.get(url, headers=headers)
    print(resp.json())
    server_ca_cert = resp.json()["serverCaCert"]["cert"]

    with open(CA_FILENAME, "w+") as ca_out:
        ca_out.write(server_ca_cert)


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


def test_connector_connection(client: FlaskClient) -> None:
    del os.environ["INSTANCE_HOST"]
    app.db = app.init_connection_pool()
    assert str(app.db.url) == "mssql+pytds://localhost"
    test_get_votes(client)
    test_cast_vote(client)
