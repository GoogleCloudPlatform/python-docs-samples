# Copyright 2015 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The Python implementation of the GRPC helloworld.Greeter client."""

import argparse

import grpc

import helloworld_pb2
import helloworld_pb2_grpc


def run(host, api_key):
    channel = grpc.insecure_channel(host)
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    metadata = []
    if api_key:
        metadata.append(("x-api-key", api_key))
    response = stub.SayHello(helloworld_pb2.HelloRequest(name="you"), metadata=metadata)
    print("Greeter client received: " + response.message)
    response = stub.SayHelloAgain(
        helloworld_pb2.HelloRequest(name="you"), metadata=metadata
    )
    print("Greeter client received: " + response.message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--host", default="localhost:50051", help="The server host.")
    parser.add_argument(
        "--api_key", default=None, help="The API key to use for the call."
    )
    args = parser.parse_args()
    run(args.host, args.api_key)
