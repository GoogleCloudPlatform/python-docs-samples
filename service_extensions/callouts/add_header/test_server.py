# Copyright 2023 Google LLC.
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

"""
# Example external processing server - Client/Test File
----
This server does two things:
 When it gets request_headers, it replaces the Host header with service-extensions.com
  and resets the path to /.
 When it gets response_headers, it adds a "hello: service-extensions" response header.
"""

from __future__ import print_function

import threading
import urllib.request

import grpc
import pytest

from server import serve
import service_pb2
import service_pb2_grpc


def get_request(end_of_stream: bool = False) -> service_pb2.HttpHeaders:
    request_header = service_pb2.HttpHeaders(
        end_of_stream=end_of_stream,
    )
    request = service_pb2.ProcessingRequest(
        request_headers=request_header, async_mode=False
    )
    return request


def get_requests_stream() -> service_pb2.HttpHeaders:
    request = get_request(False)
    yield request
    request = get_request(True)
    yield request


@pytest.fixture(scope="module")
def setup_and_teardown() -> None:
    try:
        # Start the server in a background thread
        thread = threading.Thread(target=serve)
        thread.daemon = True
        thread.start()
        # Wait for the server to start
        thread.join(timeout=5)
        yield
    finally:
        # Stop the server
        del thread


@pytest.mark.usefixtures("setup_and_teardown")
def test_server() -> None:
    try:
        with grpc.insecure_channel("0.0.0.0:8080") as channel:
            stub = service_pb2_grpc.ExternalProcessorStub(channel)
            for response in stub.Process(get_requests_stream()):
                headers = response.request_headers.response.header_mutation
                assert 'raw_value: "service-extensions.com"' in str(headers)
                assert 'key: "host"' in str(headers)
    except grpc._channel._MultiThreadedRendezvous:
        raise Exception("SetUp Error: Server not ready!")


@pytest.mark.usefixtures("setup_and_teardown")
def test_server_health_check() -> None:
    try:
        response = urllib.request.urlopen("http://0.0.0.0:80")
        assert response.read() == b""
        assert response.getcode() == 200
    except urllib.error.URLError:
        raise Exception("SetUp Error: Server not ready!")
