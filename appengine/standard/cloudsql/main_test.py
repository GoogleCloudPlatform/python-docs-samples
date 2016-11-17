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

import os
import re

import pytest
import webtest


@pytest.fixture
def main(monkeypatch):
    monkeypatch.setenv('CLOUDSQL_USER', 'root')
    monkeypatch.setenv('CLOUDSQL_PASSWORD', '')
    import main
    return main


@pytest.mark.skipif(
    not os.path.exists('/var/run/mysqld/mysqld.sock'),
    reason='Local MySQL server not available.')
def test_app(main):
    app = webtest.TestApp(main.app)
    response = app.get('/')

    assert response.status_int == 200
    assert re.search(
        re.compile(r'.*version.*', re.DOTALL),
        response.body)
