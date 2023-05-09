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
import unittest
from unittest import mock
import uuid

import flask
import google.api_core.exceptions
import main

PROJECT_ID = "my-project"
MEDIA_ID = "some-media-id"


@mock.patch("main.secretmanager.SecretManagerServiceClient")
class MainTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        # Create a fake "app" for generating test request contexts.
        self.app = flask.Flask(__name__)
        os.environ["PROJECT"] = PROJECT_ID

    def test_should_create_secret_and_version(self, secret_manager_mock):
        key_id = uuid.uuid4()
        secret_name = "the-secret-name"
        secret_manager_mock.return_value.create_secret.return_value.name = secret_name
        with self.app.test_request_context(
            method="POST",
            json={
                "mediaId": MEDIA_ID,
                "provider": "FakeProvider",
                "keyIds": [key_id],
            },
        ):
            resp = flask.make_response(main.keys(flask.request))
            self.assertEqual(resp.status_code, 200)
        secret_manager_mock.return_value.create_secret.assert_called_once_with(
            request={
                "parent": f"projects/{PROJECT_ID}",
                "secret_id": MEDIA_ID,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        secret_manager_mock.return_value.add_secret_version.assert_called_once_with(
            request={"parent": secret_name, "payload": {"data": mock.ANY}}
        )

    def test_should_create_version_for_existing_secret(self, secret_manager_mock):
        key_id = uuid.uuid4()
        secret_manager_mock.return_value.create_secret.side_effect = (
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
            self.assertEqual(resp.status_code, 200)
        secret_manager_mock.return_value.create_secret.assert_called_once_with(
            request={
                "parent": f"projects/{PROJECT_ID}",
                "secret_id": MEDIA_ID,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        secret_manager_mock.return_value.add_secret_version.assert_called_once_with(
            request={
                "parent": f"projects/{PROJECT_ID}/secrets/{MEDIA_ID}",
                "payload": {"data": mock.ANY},
            }
        )

    def test_should_fail_when_create_secret_fails(self, secret_manager_mock):
        key_id = uuid.uuid4()
        secret_manager_mock.return_value.create_secret.side_effect = (
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
            self.assertEqual(resp.status_code, 500)
        secret_manager_mock.return_value.create_secret.assert_called_once_with(
            request={
                "parent": f"projects/{PROJECT_ID}",
                "secret_id": MEDIA_ID,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        secret_manager_mock.return_value.add_secret_version.assert_not_called()

    def test_should_fail_on_get(self, secret_manager_mock):
        del secret_manager_mock
        with self.app.test_request_context(method="GET"):
            resp = flask.make_response(main.keys(flask.request))
            self.assertEqual(resp.status_code, 400)
            self.assertIn(
                "Only POST requests are supported", resp.get_json()["message"]
            )

    def test_should_fail_on_missing_request_body(self, secret_manager_mock):
        del secret_manager_mock
        with self.app.test_request_context(method="POST"):
            resp = flask.make_response(main.keys(flask.request))
            self.assertEqual(resp.status_code, 400)
            self.assertIn("no request body was provided", resp.get_json()["message"])

    def test_should_fail_on_missing_mediaid(self, secret_manager_mock):
        del secret_manager_mock
        with self.app.test_request_context(method="POST", json={"name": "test"}):
            resp = flask.make_response(main.keys(flask.request))
            self.assertEqual(resp.status_code, 400)
            self.assertIn(
                '"mediaId" field must be specified', resp.get_json()["message"]
            )

    def test_should_fail_on_missing_provider(self, secret_manager_mock):
        del secret_manager_mock
        with self.app.test_request_context(method="POST", json={"mediaId": "mid"}):
            resp = flask.make_response(main.keys(flask.request))
            self.assertEqual(resp.status_code, 400)
            self.assertIn(
                '"provider" field must be specified', resp.get_json()["message"]
            )

    def test_should_fail_on_missing_keyid(self, secret_manager_mock):
        del secret_manager_mock
        with self.app.test_request_context(
            method="POST", json={"mediaId": "mid", "provider": "FakeProvider"}
        ):
            resp = flask.make_response(main.keys(flask.request))
            self.assertEqual(resp.status_code, 400)
            self.assertIn(
                "at least one key ID must be specified", resp.get_json()["message"]
            )

    def test_should_fail_on_missing_envvar(self, secret_manager_mock):
        del secret_manager_mock
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
            self.assertEqual(resp.status_code, 400)
            self.assertIn(
                'environment variable "PROJECT" must be set',
                resp.get_json()["message"],
            )


if __name__ == "__main__":
    unittest.main()
