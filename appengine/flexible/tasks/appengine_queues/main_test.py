# Copyright 2016 Google Inc. All Rights Reserved.
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


@pytest.fixture
def app():
    import main
    main.app.testing = True
    return main.app.test_client()


def test_index(app):
    r = app.get('/')
    assert r.status_code == 200


@mock.patch('main.update_payload')
@mock.patch('main.increment_counter')
def test_set_payload(increment_counter, update_payload, app):
    payload = 'hello'

    r = app.post('/set_payload', payload)
    assert r.status_code == 200

    assert increment_counter.called
    assert update_payload.called

    r = app.get('/get_payload')
    assert r.status_code == 200
