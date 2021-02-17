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
# These unit tests mock logging.

import pytest

import main


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_no_trace_in_headers(client, capsys):
    r = client.get("/")
    assert r.status_code == 200

    out, _ = capsys.readouterr()
    print(out)
    assert "trace" not in out


def test_with_cloud_headers(client, capsys):
    r = client.get("/", headers={"X-Cloud-Trace-Context": "foo/bar"})
    assert r.status_code == 200

    out, _ = capsys.readouterr()
    print(out)
    assert "trace" in out
