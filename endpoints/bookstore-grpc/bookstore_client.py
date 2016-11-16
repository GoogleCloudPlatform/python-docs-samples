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

"""The Python GRPC Bookstore Client Example."""

import argparse

import bookstore_pb2

from google.protobuf import empty_pb2
from grpc.beta import implementations


def _add_endpoints_metadata(api_key):
  def add_metadata(metadata):
    if metadata:
      for k, v in metadata:
        yield (k, v)
    if api_key:
      yield ('x-api-key', api_key)

  return add_metadata


def _run():
  """Runs a basic ListShelves call against a GRPC server."""

  parser = argparse.ArgumentParser(
      description='List bookstore shelves',
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--host', default='localhost',
                      help='The host to connect to')
  parser.add_argument('--port', type=int, default=8000,
                      help='The port to connect to')
  parser.add_argument('--timeout', type=int, default=10,
                      help='The call timeout, in seconds')
  parser.add_argument('--api_key', help='The API key to use for the call')
  args = parser.parse_args()

  channel = implementations.insecure_channel(args.host, args.port)
  stub = bookstore_pb2.beta_create_Bookstore_stub(
      channel, metadata_transformer = _add_endpoints_metadata(args.api_key))
  shelves = stub.ListShelves(empty_pb2.Empty(), args.timeout)
  print 'ListShelves: %s' % shelves


if __name__ == '__main__':
  _run()
