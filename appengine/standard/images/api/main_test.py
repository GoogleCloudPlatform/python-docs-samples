# Copyright 2015 Google Inc. All rights reserved.
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

import mock
import pytest
import webtest

import main


@pytest.fixture
def app(testbed):
    return webtest.TestApp(main.app)


def test_img(app):
    with mock.patch('main.images') as mock_images:
        mock_images.resize.return_value = 'asdf'
        mock_images.im_feeling_lucky.return_value = 'gsdf'
        photo = main.Photo(
            id=234
        )
        photo.title = 'asdf'
        photo.full_size_image = b'123'
        photo.put()

        response = app.get('/img?id=%s' % photo.key.id())

        assert response.status_int == 200


def test_img_missing(app):
    # Bogus image id, should get error
    app.get('/img?id=123', status=404)


def test_no_img_id(app):
    # No image id, should get error
    app.get('/img', status=404)
