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

from uuid import uuid4

from google.cloud import storage

import pytest

import main


@pytest.fixture
def bucket_name():
    client = storage.Client()
    name = f"practice-folder-{uuid4().hex}"
    bucket = client.bucket(name)
    bucket.create()

    blob_one = bucket.blob("blob-one")
    blob_one.upload_from_string("This is blob ONE")

    blob_two = bucket.blob("blob-two")
    blob_two.upload_from_string("This is blob TWO")

    yield name

    bucket.delete(force=True)


def test_list_blobs(bucket_name, capsys):
    blobs = main.list_blobs(bucket_name)

    assert len(blobs) == 2
    assert "blob-one" in blobs
    assert "blob-two" in blobs

    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    assert len(lines) == 3
    assert "blob-one" in lines
    assert "blob-two" in lines
    assert lines[2] == ""  # Trailing newline from print leaves empty line
