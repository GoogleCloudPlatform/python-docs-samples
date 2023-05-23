#!/usr/bin/env python

# Copyright 2021 Google LLC
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

import re
import uuid

from google.cloud import storage

import pytest

from snippets import main


@pytest.fixture(scope="module")
def test_bucket():
    """Yields a bucket that is deleted after the test completes."""
    bucket = None
    while bucket is None or bucket.exists():
        bucket_name = f"bucket-downscoping-test-{uuid.uuid4()}"
        bucket = storage.Client().bucket(bucket_name)
    bucket = storage.Client().create_bucket(bucket.name)
    yield bucket
    bucket.delete(force=True)


@pytest.fixture(scope="module")
def test_blob(test_bucket):
    """Yields a blob that is deleted after the test completes."""
    bucket = test_bucket
    blob = bucket.blob("customer-a-data.txt")
    blob.upload_from_string("hello world")
    yield blob


def test_main(capsys, test_blob):
    main(test_blob.bucket.name, test_blob.name)
    out, err = capsys.readouterr()

    assert not re.search(
        r"error", out, re.IGNORECASE
    ), f"Error detected in the output: {out}"
    assert re.search(r"Testing.*Done", out, re.DOTALL), f"Unexpected output: {out}"
