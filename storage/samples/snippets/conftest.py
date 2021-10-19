#!/usr/bin/env python

# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
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

import os
import time
import uuid

from google.cloud import storage
import pytest


@pytest.fixture(scope="function")
def bucket():
    """Yields a bucket that is deleted after the test completes."""
    # The new projects enforces uniform bucket level access, so
    # we need to use the old main project for now.
    original_value = os.environ['GOOGLE_CLOUD_PROJECT']
    os.environ['GOOGLE_CLOUD_PROJECT'] = os.environ['MAIN_GOOGLE_CLOUD_PROJECT']
    bucket = None
    while bucket is None or bucket.exists():
        bucket_name = f"uniform-bucket-level-access-{uuid.uuid4().hex}"
        bucket = storage.Client().bucket(bucket_name)
    bucket.create()
    yield bucket
    time.sleep(3)
    bucket.delete(force=True)
    # Set the value back.
    os.environ['GOOGLE_CLOUD_PROJECT'] = original_value
