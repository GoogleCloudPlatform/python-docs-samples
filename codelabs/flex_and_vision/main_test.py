# Copyright 2017 Google Inc. All Rights Reserved.
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
import six

import main

TEST_PHOTO_URL = (
    'https://upload.wikimedia.org/wikipedia/commons/5/5e/'
    'John_F._Kennedy%2C_White_House_photo_portrait%2C_looking_up.jpg')


@pytest.fixture
def app():
    main.app.testing = True
    client = main.app.test_client()
    return client


def test_index(app):
    r = app.get('/')
    assert r.status_code == 200


def test_upload_photo(app):
    test_photo_data = requests.get(TEST_PHOTO_URL).content

    r = app.post(
        '/upload_photo',
        data={
            'file': (six.BytesIO(test_photo_data), 'flex_and_vision.jpg')
        }
    )

    assert r.status_code == 302
