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
from __future__ import print_function

import threading
import urllib.request

import grpc
import pytest

import server
import service_pb2
import service_pb2_grpc


def get_request(
    end_of_stream: bool = False, is_request_header: bool = True
) -> service_pb2.ProcessingRequest:
    "Returns a ProcessingRequest"
    _headers = service_pb2.HttpHeaders(
        end_of_stream=end_of_stream,
    )
    if is_request_header:
        request = service_pb2.ProcessingRequest(
            request_headers=_headers, async_mode=False
        )
    else:
        request = service_pb2.ProcessingRequest(
            response_headers=_headers, async_mode=False
        )
    return request


def get_requests_stream() -> service_pb2.ProcessingRequest:
    request = get_request(end_of_stream=False, is_request_header=True)
    yield request
    request = get_request(end_of_stream=False, is_request_header=False)
    yield request
    request = get_request(end_of_stream=True)
    yield request


@pytest.fixture(scope="module")
def setup_and_teardown() -> None:
    try:
        # Start the server in a background thread
        thread = threading.Thread(target=server.serve)
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
        with grpc.insecure_channel(
            f"0.0.0.0:{server.EXT_PROC_INSECURE_PORT}"
        ) as channel:
            stub = service_pb2_grpc.ExternalProcessorStub(channel)
            for response in stub.Process(get_requests_stream()):
                str_message = str(response)
                if "request_headers" in str_message:
                    assert 'raw_value: "service-extensions.com"' in str_message
                    assert 'key: "host"' in str_message
                elif "response_headers" in str_message:
                    assert 'raw_value: "service-extensions"' in str_message
                    assert 'key: "hello"' in str_message
    except grpc._channel._MultiThreadedRendezvous:
        raise Exception("Setup Error: Server not ready!")


@pytest.mark.usefixtures("setup_and_teardown")
def test_server_health_check() -> None:
    try:
        response = urllib.request.urlopen(f"http://0.0.0.0:{server.HEALTH_CHECK_PORT}")
        assert response.read() == b""
        assert response.getcode() == 200
    except urllib.error.URLError:
        raise Exception("Setup Error: Server not ready!")


if __name__ == "__main__":
    # Run the gRPC service
    test_server()
