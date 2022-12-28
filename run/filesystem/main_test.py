# Copyright 2021 Google LLC
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

import os

import pytest

import main

# Tests use the sample's directory as the mount point directory
mnt_dir = os.environ.get("MNT_DIR", os.getcwd())
filename = os.environ.get("FILENAME", "Dockerfile")


@pytest.fixture
def client():
    main.mnt_dir = os.getcwd()
    main.app.testing = True
    return main.app.test_client()


def test_index(client):
    r = client.get("/")

    assert r.status_code == 302


def test_mnt_path(client):
    r = client.get(mnt_dir)

    assert filename in r.data.decode()
    assert r.status_code == 200


def test_non_mnt_path(client):
    r = client.get("/not/the/right/path")

    assert r.status_code == 302


def test_file_access(client):
    full_path = os.path.join(mnt_dir, filename)
    r = client.get(full_path)

    assert "ENTRYPOINT" in r.data.decode()
    assert r.status_code == 200


def test_no_file_access(client):
    full_path = os.path.join(mnt_dir, 'not-a-file')
    r = client.get(full_path)

    assert r.status_code == 404
    assert "Error retrieving file" in r.data.decode()
