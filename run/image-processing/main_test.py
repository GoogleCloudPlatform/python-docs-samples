# Copyright 2019 Google, LLC.
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

# NOTE:
# These tests are unit tests that mock Pub/Sub.
import base64
import json
from unittest import mock
import uuid

import pytest

import main


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_empty_payload(client):
    r = client.post("/", json="")
    assert r.status_code == 400


def test_invalid_payload(client):
    r = client.post("/", json={"nomessage": "invalid"})
    assert r.status_code == 400


def test_invalid_mimetype(client):
    r = client.post("/", json="{ message: true }")
    assert r.status_code == 400


@mock.patch("image.blur_offensive_images", mock.MagicMock(return_value=204))
def test_minimally_valid_message(client):
    data_json = json.dumps({"name": True, "bucket": True})
    data = base64.b64encode(data_json.encode()).decode()

    r = client.post("/", json={"message": {"data": data}})
    assert r.status_code == 204


def test_call_to_blur_image(client, capsys):
    filename = str(uuid.uuid4())
    blur_bucket = "blurred-bucket-" + str(uuid.uuid4())

    data_json = json.dumps({"name": filename, "bucket": blur_bucket})
    data = base64.b64encode(data_json.encode()).decode()

    r = client.post("/", json={"message": {"data": data}})
    assert r.status_code == 204

    out, _ = capsys.readouterr()
    assert f"The image {filename} was detected as OK" in out
