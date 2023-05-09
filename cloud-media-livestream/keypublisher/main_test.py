# Copyright 2023 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the main key publisher module."""

import os
import uuid

import flask
import google.api_core.exceptions
import main
import pytest

PROJECT_ID = "my-project"
MEDIA_ID = "some-media-id"

@pytest.fixture()
def app():
    app = flask.Flask(__name__)
    os.environ["PROJECT"] = PROJECT_ID
    yield app

@pytest.fixture()
def mock(mocker):
  mock = mocker.patch("main.secretmanager.SecretManagerServiceClient")
  yield mock

class TestMain:
    @pytest.fixture(autouse=True)
    def _get_app(self, app):
        self.app = app
        
    @pytest.fixture(autouse=True)
    def _mock(self, mock):
        self.secret_manager_mock = mock
        
    def test_should_create_secret_and_version(self, mocker):
        key_id = uuid.uuid4()
        secret_name = "the-secret-name"
        self.secret_manager_mock.return_value.create_secret.return_value.name = secret_name
        with self.app.test_request_context(
            method="POST",
            json={
                "mediaId": MEDIA_ID,
                "provider": "FakeProvider",
                "keyIds": [key_id],
            },
        ):
            resp = flask.make_response(main.keys(flask.request))
            assert resp.status_code == 200
        self.secret_manager_mock.return_value.create_secret.assert_called_once_with(
            request={
                "parent": f"projects/{PROJECT_ID}",
                "secret_id": MEDIA_ID,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        self.secret_manager_mock.return_value.add_secret_version.assert_called_once_with(
            request={"parent": secret_name, "payload": {"data": mocker.ANY}}
        )

    def test_should_create_version_for_existing_secret(self, mocker):
        key_id = uuid.uuid4()
        self.secret_manager_mock.return_value.create_secret.side_effect = (
            google.api_core.exceptions.AlreadyExists("secret already exists")
        )
        with self.app.test_request_context(
            method="POST",
            json={
                "mediaId": MEDIA_ID,
                "provider": "FakeProvider",
                "keyIds": [key_id],
            },
        ):
            resp = flask.make_response(main.keys(flask.request))
            assert resp.status_code == 200
        self.secret_manager_mock.return_value.create_secret.assert_called_once_with(
            request={
                "parent": f"projects/{PROJECT_ID}",
                "secret_id": MEDIA_ID,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        self.secret_manager_mock.return_value.add_secret_version.assert_called_once_with(
            request={
                "parent": f"projects/{PROJECT_ID}/secrets/{MEDIA_ID}",
                "payload": {"data": mocker.ANY},
            }
        )

    def test_should_fail_when_create_secret_fails(self):
        key_id = uuid.uuid4()
        self.secret_manager_mock.return_value.create_secret.side_effect = (
            google.api_core.exceptions.InternalServerError(
                "fake error, please ignore, testing error handling"
            )
        )
        with self.app.test_request_context(
            method="POST",
            json={
                "mediaId": MEDIA_ID,
                "provider": "FakeProvider",
                "keyIds": [key_id],
            },
        ):
            resp = flask.make_response(main.keys(flask.request))
            assert resp.status_code == 500
        self.secret_manager_mock.return_value.create_secret.assert_called_once_with(
            request={
                "parent": f"projects/{PROJECT_ID}",
                "secret_id": MEDIA_ID,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        self.secret_manager_mock.return_value.add_secret_version.assert_not_called()

    def test_should_fail_on_get(self):
        del self.secret_manager_mock
        with self.app.test_request_context(method="GET"):
            resp = flask.make_response(main.keys(flask.request))
            assert resp.status_code == 400
            assert "Only POST requests are supported" in resp.get_json()["message"]

    def test_should_fail_on_missing_request_body(self):
        del self.secret_manager_mock
        with self.app.test_request_context(method="POST"):
            resp = flask.make_response(main.keys(flask.request))
            assert resp.status_code == 400
            assert "no request body was provided" in resp.get_json()["message"]

    def test_should_fail_on_missing_mediaid(self):
        del self.secret_manager_mock
        with self.app.test_request_context(method="POST", json={"name": "test"}):
            resp = flask.make_response(main.keys(flask.request))
            assert resp.status_code == 400
            assert '"mediaId" field must be specified' in resp.get_json()["message"]

    def test_should_fail_on_missing_provider(self):
        del self.secret_manager_mock
        with self.app.test_request_context(method="POST", json={"mediaId": "mid"}):
            resp = flask.make_response(main.keys(flask.request))
            assert resp.status_code == 400
            assert '"provider" field must be specified' in resp.get_json()["message"]

    def test_should_fail_on_missing_keyid(self):
        del self.secret_manager_mock
        with self.app.test_request_context(
            method="POST", json={"mediaId": "mid", "provider": "FakeProvider"}
        ):
            resp = flask.make_response(main.keys(flask.request))
            assert resp.status_code == 400
            assert "at least one key ID must be specified" in resp.get_json()["message"]

    def test_should_fail_on_missing_envvar(self):
        del self.secret_manager_mock
        del os.environ["PROJECT"]
        key_id = uuid.uuid4()
        with self.app.test_request_context(
            method="POST",
            json={
                "mediaId": MEDIA_ID,
                "provider": "FakeProvider",
                "keyIds": [key_id],
            },
        ):
            resp = flask.make_response(main.keys(flask.request))
            assert resp.status_code == 400
            assert (
                'environment variable "PROJECT" must be set'
                in resp.get_json()["message"]
            )
