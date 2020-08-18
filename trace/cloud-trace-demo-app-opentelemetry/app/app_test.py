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
A sample app demonstrating Stackdriver Trace
"""

import httpretty
import mock

import app
import pdb


def test_send_response():
    pdb.set_trace()
    service_keyword = 'Hello'
    app.app.testing = True
    app.app.config['keyword'] = service_keyword
    app.app.config['endpoint'] = ''
    client = app.app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    assert service_keyword in resp.data.decode('utf-8')


def test_traces():

    exporter = mock.Mock()
    app.SimpleExportSpanProcessor(exporter)

    client = app.app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200

