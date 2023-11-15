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
# [START serviceextensions_callout_add_header]
"""
# Example external processing server
----
This server does two things:
* When it receives a `request_headers`, it replaces the Host header
        with "host: service-extensions.com" and resets the path to /
* When it receives a `response_headers`, it adds
        a "hello: service-extensions" response header

This server also has optional SSL authentication.
"""
# [START serviceextensions_callout_add_header_imports]
from concurrent import futures
from http.server import BaseHTTPRequestHandler, HTTPServer

from typing import Iterator, List, Tuple

import grpc

from grpc import ServicerContext

import service_pb2
import service_pb2_grpc

# Backend services on GCE VMs, GKE and hybrid use this port.
EXT_PROC_SECURE_PORT = 8443
# Backend services on Cloud Run use this port.
EXT_PROC_INSECURE_PORT = 8080
# Cloud health checks use this port.
HEALTH_CHECK_PORT = 8000
# Example SSL Credentials for gRPC server
# PEM-encoded private key & PEM-encoded certificate chain
SERVER_CERTIFICATE = open("ssl_creds/localhost.crt", "rb").read()
SERVER_CERTIFICATE_KEY = open("ssl_creds/localhost.key", "rb").read()
ROOT_CERTIFICATE = open("ssl_creds/root.crt", "rb").read()


# [END serviceextensions_callout_add_header_imports]
# [START serviceextensions_callout_add_header_main]
def add_headers_mutation(
    headers: List[Tuple[str, str]], clear_route_cache: bool = False
) -> service_pb2.HeadersResponse:
    """
    Returns an ext_proc HeadersResponse for adding a list of headers.
    clear_route_cache should be set to influence service selection for route
    extensions.
    """
    response_header_mutation = service_pb2.HeadersResponse()
    response_header_mutation.response.header_mutation.set_headers.extend(
        [
            service_pb2.HeaderValueOption(
                header=service_pb2.HeaderValue(key=k, raw_value=bytes(v, "utf-8"))
            )
            for k, v in headers
        ]
    )
    if clear_route_cache:
        response_header_mutation.response.clear_route_cache = True
    return response_header_mutation


class CalloutProcessor(service_pb2_grpc.ExternalProcessorServicer):
    def Process(
        self,
        request_iterator: Iterator[service_pb2.ProcessingRequest],
        context: ServicerContext,
    ) -> Iterator[service_pb2.ProcessingResponse]:
        "Process the client request and add example headers"
        for request in request_iterator:
            if request.HasField("response_headers"):
                response_header_mutation = add_headers_mutation(
                    [("hello", "service-extensions")]
                )
                yield service_pb2.ProcessingResponse(
                    response_headers=response_header_mutation
                )
            elif request.HasField("request_headers"):
                request_header_mutation = add_headers_mutation(
                    [("host", "service-extensions.com"), (":path", "/")],
                    clear_route_cache=True,
                )
                yield service_pb2.ProcessingResponse(
                    request_headers=request_header_mutation
                )


class HealthCheckServer(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        "Returns an empty page with 200 status code"
        self.send_response(200)
        self.end_headers()


def serve() -> None:
    "Run gRPC server and Health check server"
    health_server = HTTPServer(("0.0.0.0", HEALTH_CHECK_PORT), HealthCheckServer)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    service_pb2_grpc.add_ExternalProcessorServicer_to_server(CalloutProcessor(), server)
    server_credentials = grpc.ssl_server_credentials(
        private_key_certificate_chain_pairs=[
            (SERVER_CERTIFICATE_KEY, SERVER_CERTIFICATE)
        ]
    )
    server.add_secure_port("0.0.0.0:%d" % EXT_PROC_SECURE_PORT, server_credentials)
    server.add_insecure_port("0.0.0.0:%d" % EXT_PROC_INSECURE_PORT)
    server.start()
    print(
        "Server started, listening on %d and %d"
        % (EXT_PROC_SECURE_PORT, EXT_PROC_INSECURE_PORT)
    )
    try:
        health_server.serve_forever()
    except KeyboardInterrupt:
        print("Server interrupted")
    finally:
        server.stop()
        health_server.server_close()


# [END serviceextensions_callout_add_header_main]
# [END serviceextensions_callout_add_header]
if __name__ == "__main__":
    # Run the gRPC service
    serve()
