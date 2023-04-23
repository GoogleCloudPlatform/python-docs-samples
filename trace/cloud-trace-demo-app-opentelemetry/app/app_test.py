# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
A sample app demonstrating Google Cloud Trace
"""
import os

from unittest import mock

import app


def test_traces():
    expected = "Lorem ipsum dolor sit amet"
    os.environ["KEYWORD"] = expected
    app.app.testing = True
    exporter = mock.Mock()
    app.configure_exporter(exporter)
    client = app.app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert expected in resp.data.decode('utf-8')
