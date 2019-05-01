# Copyright 2015 Google Inc. All Rights Reserved.
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

import pytest
import requests
from six import BytesIO

import main


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_index(client):
    r = client.get('/')
    assert r.status_code == 200


def test_upload(client):
    # Upload a simple file
    file_content = b"This is some test content."

    r = client.post(
        '/upload',
        data={
            'file': (BytesIO(file_content), 'example.txt')
        }
    )

    assert r.status_code == 200

    # The app should return the public cloud storage URL for the uploaded
    # file. Download and verify it.
    cloud_storage_url = r.data.decode('utf-8')
    r = requests.get(cloud_storage_url)
    assert r.text.encode('utf-8') == file_content
