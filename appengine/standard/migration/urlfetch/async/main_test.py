# Copyright 2020 Google LLC
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

import main
import pytest
import sys


@pytest.mark.skipif(sys.version_info < (3, 0), reason="no urlfetch adapter in test env")
def test_index():
    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert 'Google is built by a large team ' in r.data.decode('utf-8')

    r = client.get('/callback')
    assert r.status_code == 200
    assert 'Response number 1 is ' in r.data.decode('utf-8')
    assert 'Response number 2 is ' in r.data.decode('utf-8')
    assert 'Response number 3 is ' in r.data.decode('utf-8')
    assert 'Response number 4 is ' in r.data.decode('utf-8')
