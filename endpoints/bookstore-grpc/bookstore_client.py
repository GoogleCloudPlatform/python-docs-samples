# Copyright 2016 Google Inc. All Rights Reserved.
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

"""The Python gRPC Bookstore Client Example."""
import argparse

from google.protobuf import empty_pb2
import grpc

import bookstore_pb2_grpc


def run(host, port, api_key, auth_token, timeout, use_tls, servername_override, ca_path):
    """Makes a basic ListShelves call against a gRPC Bookstore server."""

    if use_tls:
        with open(ca_path, 'rb') as f:
            creds = grpc.ssl_channel_credentials(f.read())
        channel_opts = ()
        if servername_override:
            channel_opts += ((
                        'grpc.ssl_target_name_override', servername_override,),)
        channel = grpc.secure_channel(f'{host}:{port}', creds, channel_opts)
    else:
        channel = grpc.insecure_channel(f'{host}:{port}')

    stub = bookstore_pb2_grpc.BookstoreStub(channel)
    metadata = []
    if api_key:
        metadata.append(('x-api-key', api_key))
    if auth_token:
        metadata.append(('authorization', 'Bearer ' + auth_token))
    shelves = stub.ListShelves(empty_pb2.Empty(), timeout, metadata=metadata)
    print(f'ListShelves: {shelves}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--host', default='localhost', help='The host to connect to')
    parser.add_argument(
        '--port', type=int, default=8000, help='The port to connect to')
    parser.add_argument(
        '--timeout', type=int, default=10, help='The call timeout, in seconds')
    parser.add_argument(
        '--api_key', default=None, help='The API key to use for the call')
    parser.add_argument(
        '--servername', type=str, default='', help='The servername to use to call the API.')
    parser.add_argument(
        '--ca_path', type=str, default="../roots.pem", help='The path to the CA.')
    parser.add_argument(
        '--auth_token', default=None,
        help='The JWT auth token to use for the call')
    parser.add_argument(
        '--use_tls', type=bool, default=False,
        help='Enable when the server requires TLS')
    args = parser.parse_args()
    run(args.host, args.port, args.api_key, args.auth_token, args.timeout, args.use_tls, args.servername, args.ca_path)
