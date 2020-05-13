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

import os

import pytest

import main


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_broken_handler(client):
    with pytest.raises(Exception) as e:
        client.get("/")

    assert "Missing required service parameter" in str(e.value)


def test_broken_handler_with_env_variable(client):
    os.environ["NAME"] = "Foo"
    r = client.get("/")

    assert r.data.decode() == "Hello Foo"
    assert r.status_code == 200


def test_improved_handler_no_env_variable(client):
    os.environ["NAME"] = ""
    r = client.get("/improved")

    assert r.data.decode() == "Hello World"
    assert r.status_code == 200


def test_improved_handler_with_env_variable(client):
    os.environ["NAME"] = "Foo"
    r = client.get("/improved")

    assert r.data.decode() == "Hello Foo"
    assert r.status_code == 200
