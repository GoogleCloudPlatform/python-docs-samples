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

from google.protobuf import timestamp_pb2
import pytest

import create_cdn_key
import create_cdn_key_akamai
import delete_cdn_key
import get_cdn_key
import list_cdn_keys
import update_cdn_key
import update_cdn_key_akamai
import utils

location = "us-central1"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
now = timestamp_pb2.Timestamp()
now.GetCurrentTime()

media_cdn_key_id = f"python-test-media-key-{uuid.uuid4().hex[:5]}-{now.seconds}"
cloud_cdn_key_id = f"python-test-cloud-key-{uuid.uuid4().hex[:5]}-{now.seconds}"
akamai_cdn_key_id = f"python-test-akamai-key-{uuid.uuid4().hex[:5]}-{now.seconds}"

hostname = "cdn.example.com"
updated_hostname = "updated.example.com"
key_name = "my-key"

media_cdn_private_key = "MTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMjM0NTY3ODkwMTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMjM0NTY3ODkwMTIzNA"
updated_media_cdn_private_key = (
    "ZZZzNDU2Nzg5MDEyMzQ1Njc4OTAxzg5MDEyMzQ1Njc4OTAxMjM0NTY3DkwMTIZZZ"
)
cloud_cdn_private_key = "VGhpcyBpcyBhIHRlc3Qgc3RyaW5nLg=="
updated_cloud_cdn_private_key = "VGhpcyBpcyBhbiB1cGRhdGVkIHRlc3Qgc3RyaW5nLg=="
akamai_key = cloud_cdn_private_key
updated_akamai_key = updated_cloud_cdn_private_key


@pytest.mark.skip()
def test_cdn_key_operations(capsys: pytest.fixture) -> None:

    utils.delete_stale_cdn_keys(project_id, location)

    # Media CDN key tests

    create_cdn_key.create_cdn_key(
        project_id,
        location,
        media_cdn_key_id,
        hostname,
        key_name,
        media_cdn_private_key,
        False,
    )
    out, _ = capsys.readouterr()
    assert media_cdn_key_id in out

    list_cdn_keys.list_cdn_keys(project_id, location)
    out, _ = capsys.readouterr()
    assert media_cdn_key_id in out

    # Update the hostname and private key; the private key value
    # is not returned by the client
    response = update_cdn_key.update_cdn_key(
        project_id,
        location,
        media_cdn_key_id,
        updated_hostname,
        key_name,
        updated_media_cdn_private_key,
        False,
    )
    out, _ = capsys.readouterr()
    assert media_cdn_key_id in out
    assert updated_hostname in response.hostname

    get_cdn_key.get_cdn_key(project_id, location, media_cdn_key_id)
    out, _ = capsys.readouterr()
    assert media_cdn_key_id in out

    delete_cdn_key.delete_cdn_key(project_id, location, media_cdn_key_id)
    out, _ = capsys.readouterr()
    assert "Deleted CDN key" in out

    # Cloud CDN key tests

    create_cdn_key.create_cdn_key(
        project_id,
        location,
        cloud_cdn_key_id,
        hostname,
        key_name,
        cloud_cdn_private_key,
        True,
    )
    out, _ = capsys.readouterr()
    assert cloud_cdn_key_id in out

    list_cdn_keys.list_cdn_keys(project_id, location)
    out, _ = capsys.readouterr()
    assert cloud_cdn_key_id in out

    # Update the hostname and private key; the private key value
    # is not returned by the client
    response = update_cdn_key.update_cdn_key(
        project_id,
        location,
        cloud_cdn_key_id,
        updated_hostname,
        key_name,
        updated_cloud_cdn_private_key,
        True,
    )
    out, _ = capsys.readouterr()
    assert cloud_cdn_key_id in out
    assert updated_hostname in response.hostname

    get_cdn_key.get_cdn_key(project_id, location, cloud_cdn_key_id)
    out, _ = capsys.readouterr()
    assert cloud_cdn_key_id in out

    delete_cdn_key.delete_cdn_key(project_id, location, cloud_cdn_key_id)
    out, _ = capsys.readouterr()
    assert "Deleted CDN key" in out

    # Akamai CDN key tests

    create_cdn_key_akamai.create_cdn_key_akamai(
        project_id,
        location,
        akamai_cdn_key_id,
        hostname,
        akamai_key,
    )
    out, _ = capsys.readouterr()
    assert akamai_cdn_key_id in out

    list_cdn_keys.list_cdn_keys(project_id, location)
    out, _ = capsys.readouterr()
    assert akamai_cdn_key_id in out

    # Update the hostname and private key; the private key value
    # is not returned by the client
    response = update_cdn_key_akamai.update_cdn_key_akamai(
        project_id,
        location,
        akamai_cdn_key_id,
        updated_hostname,
        updated_akamai_key,
    )
    out, _ = capsys.readouterr()
    assert akamai_cdn_key_id in out
    assert updated_hostname in response.hostname

    get_cdn_key.get_cdn_key(project_id, location, akamai_cdn_key_id)
    out, _ = capsys.readouterr()
    assert akamai_cdn_key_id in out

    delete_cdn_key.delete_cdn_key(project_id, location, akamai_cdn_key_id)
    out, _ = capsys.readouterr()
    assert "Deleted CDN key" in out
