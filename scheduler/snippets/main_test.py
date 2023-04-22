# Copyright 2019 Google LLC
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


@pytest.fixture
def app():
    import main

    main.app.testing = True
    return main.app.test_client()


def test_index(app):
    r = app.get("/")
    assert r.status_code == 200


def test_log_payload(capsys, app):
    payload = "test_payload"

    r = app.post("/log_payload", data=payload)
    assert r.status_code == 200

    out, _ = capsys.readouterr()
    assert payload in out


def test_empty_payload(capsys, app):
    r = app.post("/log_payload")
    assert r.status_code == 200

    out, _ = capsys.readouterr()
    assert "empty payload" in out
