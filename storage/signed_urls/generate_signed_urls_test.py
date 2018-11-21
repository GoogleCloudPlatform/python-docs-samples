# Copyright 2018 Google, Inc.
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

from google.cloud import storage
import pytest
import requests

import generate_signed_urls

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']


@pytest.fixture
def test_blob():
    """Provides a pre-existing blob in the test bucket."""
    bucket = storage.Client().bucket(BUCKET)
    blob = bucket.blob('storage_snippets_test_sigil')
    blob.upload_from_string('Hello, is it me you\'re looking for?')
    return blob


def test_generate_get_signed_url(test_blob, capsys):
    get_signed_url = generate_signed_urls.generate_signed_url(
        service_account_file=GOOGLE_APPLICATION_CREDENTIALS,
        bucket_name=BUCKET, object_name=test_blob.name,
        expiration=60)
    response = requests.get(get_signed_url)
    assert response.ok
