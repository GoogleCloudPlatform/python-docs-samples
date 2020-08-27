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


def test_send_response():
    service_keyword = "Hello"
    app.app.testing = True
    app.app.config['keyword'] = service_keyword
    app.app.config['endpoint'] = ""
    client = app.app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    assert service_keyword in resp.data.decode('utf-8')


@httpretty.activate
def test_request_url_with_trace_context():
    service1_keyword = "World"
    service2_url = "http://example.com"
    service2_keyword = "Hello"
    app.app.testing = True
    app.app.config['keyword'] = service1_keyword
    app.app.config['endpoint'] = service2_url

    def request_callback(request, uri, response_headers):
        # Assert that the request is sent with a trace context
        assert request.headers.get("X-Cloud-Trace-Context")
        return [200, response_headers, service2_keyword]

    httpretty.register_uri(httpretty.GET, service2_url, body=request_callback)
    exporter = mock.Mock()
    app.createMiddleWare(exporter)

    client = app.app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    # Assert that the response is a concatenation of responses from both services
    assert service2_keyword + service1_keyword in resp.data.decode('utf-8')
