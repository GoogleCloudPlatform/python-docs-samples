# Copyright 2020 Google, LLC.
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

import pytest

import main  # noqa I100  for parent lint


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_markdown_handler(client):
    data_input = "**strong text**"
    r = client.post("/", data=data_input)

    assert r.status_code == 200
    assert "<p><strong>strong text</strong></p>" == r.data.decode()

    data_input = (
        '<a onblur="alert(secret)" href="http://www.google.com">Google</a>'
    )
    expect = '<p><a href="http://www.google.com">Google</a></p>'
    r = client.post("/", data=data_input)
    assert r.status_code == 200
    assert expect in r.data.decode()
