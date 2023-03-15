# Copyright 2016 Google LLC.
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

import pytest
import responses


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv('GA_TRACKING_ID', '1234')

    import main

    main.app.testing = True
    return main.app.test_client()


@responses.activate
def test_tracking(app):
    responses.add(
        responses.POST,
        re.compile(r'.*'),
        body='{}',
        content_type='application/json')

    r = app.get('/')

    assert r.status_code == 200
    assert 'Event tracked' in r.data.decode('utf-8')

    assert len(responses.calls) == 1
    request_body = responses.calls[0].request.body
    assert 'tid=1234' in request_body
    assert 'ea=test+action' in request_body
