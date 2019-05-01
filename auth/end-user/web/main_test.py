# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

import main

# Note: samples that do end-user auth are difficult to test in an automated
# way. These tests are basic sanity checks.


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_index_wo_credentials(client):
    r = client.get('/')
    assert r.status_code == 302
    assert r.headers['location'].endswith('/authorize')


def test_authorize(client):
    r = client.get('/authorize')
    assert r.status_code == 302
    assert r.headers['location'].startswith('https://accounts.google.com')
