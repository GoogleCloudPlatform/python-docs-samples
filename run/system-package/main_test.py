# Copyright 2019 Google, LLC.
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

# NOTE:
# These unit tests mock subprocess.run

import main
import mock
import pytest


class SubprocessOject:
    def __init__(self, data=None):
        self.stdout = data


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_empty_query_string(client):
    r = client.get('/diagram.png')
    assert r.status_code == 400


def test_empty_dot_parameter(client):
    r = client.get('/diagram.png?dot=')
    assert r.status_code == 400


@mock.patch('main.subprocess.run',
            mock.MagicMock(return_value=SubprocessOject()))
def test_bad_dot_parameter(client):
    r = client.get('/diagram.png?dot=digraph')
    assert r.status_code == 400


@mock.patch('main.subprocess.run',
            mock.MagicMock(return_value=SubprocessOject('Image')))
def test_good_dot_parameter(client):
    r = client.get(
        '/diagram.png?dot=digraph G { A -> {B, C, D} -> {F} }')
    assert r.status_code == 200
