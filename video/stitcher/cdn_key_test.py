# Copyright 2022 Google Inc. All Rights Reserved.
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

import os
import uuid

from google.api_core.exceptions import NotFound
import pytest

import create_cdn_key
import delete_cdn_key
import get_cdn_key
import list_cdn_keys
import update_cdn_key

location = "us-central1"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
gcdn_cdn_key_id = f"my-python-test-cdn-key-{uuid.uuid4()}"
akamai_cdn_key_id = f"my-python-test-cdn-key-{uuid.uuid4()}"

hostname = "cdn.example.com"
updated_hostname = "updated.example.com"

gcdn_key_name = "gcdn-key"
gcdn_private_key = "VGhpcyBpcyBhIHRlc3Qgc3RyaW5nLg=="
updated_gcdn_private_key = "VGhpcyBpcyBhbiB1cGRhdGVkIHRlc3Qgc3RyaW5nLg=="
akamai_key = gcdn_private_key
updated_akamai_key = updated_gcdn_private_key


def test_cdn_key_operations(capsys: pytest.fixture) -> None:

    try:
        delete_cdn_key.delete_cdn_key(project_id, location, gcdn_cdn_key_id)
    except NotFound as e:
        print(f"Ignoring NotFound, details: {e}")
    out, _ = capsys.readouterr()

    try:
        delete_cdn_key.delete_cdn_key(project_id, location, akamai_cdn_key_id)
    except NotFound as e:
        print(f"Ignoring NotFound, details: {e}")
    out, _ = capsys.readouterr()

    # GCDN CDN key tests

    create_cdn_key.create_cdn_key(
        project_id,
        location,
        gcdn_cdn_key_id,
        hostname,
        gcdn_key_name,
        gcdn_private_key,
    )
    out, _ = capsys.readouterr()
    assert gcdn_cdn_key_id in out

    list_cdn_keys.list_cdn_keys(project_id, location)
    out, _ = capsys.readouterr()
    assert gcdn_cdn_key_id in out

    # Update the hostname only
    response = update_cdn_key.update_cdn_key(
        project_id, location, gcdn_cdn_key_id, updated_hostname
    )
    out, _ = capsys.readouterr()
    assert gcdn_cdn_key_id in out
    assert updated_hostname in response.hostname

    # Update the private key; the private key value is not returned by the client
    response = update_cdn_key.update_cdn_key(
        project_id,
        location,
        gcdn_cdn_key_id,
        hostname,
        gcdn_key_name,
        updated_gcdn_private_key,
    )
    out, _ = capsys.readouterr()
    assert gcdn_cdn_key_id in out

    get_cdn_key.get_cdn_key(project_id, location, gcdn_cdn_key_id)
    out, _ = capsys.readouterr()
    assert gcdn_cdn_key_id in out

    delete_cdn_key.delete_cdn_key(project_id, location, gcdn_cdn_key_id)
    out, _ = capsys.readouterr()
    assert "Deleted CDN key" in out

    # Akamai CDN key tests

    create_cdn_key.create_cdn_key(
        project_id,
        location,
        akamai_cdn_key_id,
        hostname,
        akamai_token_key=akamai_key,
    )
    out, _ = capsys.readouterr()
    assert akamai_cdn_key_id in out

    list_cdn_keys.list_cdn_keys(project_id, location)
    out, _ = capsys.readouterr()
    assert akamai_cdn_key_id in out

    # Update the hostname only
    response = update_cdn_key.update_cdn_key(
        project_id, location, akamai_cdn_key_id, updated_hostname
    )
    out, _ = capsys.readouterr()
    assert akamai_cdn_key_id in out
    assert updated_hostname in response.hostname

    # Update the private key; the private key value is not returned by the client
    response = update_cdn_key.update_cdn_key(
        project_id,
        location,
        akamai_cdn_key_id,
        hostname,
        akamai_token_key=updated_akamai_key,
    )
    out, _ = capsys.readouterr()
    assert akamai_cdn_key_id in out

    get_cdn_key.get_cdn_key(project_id, location, akamai_cdn_key_id)
    out, _ = capsys.readouterr()
    assert akamai_cdn_key_id in out

    delete_cdn_key.delete_cdn_key(project_id, location, akamai_cdn_key_id)
    out, _ = capsys.readouterr()
    assert "Deleted CDN key" in out
