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

"""The Python gRPC Bookstore Server Example."""

import argparse
import time

from google.protobuf import struct_pb2

import bookstore
from generated_pb2 import bookstore_pb2
import status

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class BookstoreServicer(bookstore_pb2.BetaBookstoreServicer):
    """Implements the bookstore API server."""
    def __init__(self, store):
        self._store = store

    def ListShelves(self, unused_request, context):
        with status.context(context):
            response = bookstore_pb2.ListShelvesResponse()
            response.shelves.extend(self._store.list_shelf())
            return response

    def CreateShelf(self, request, context):
        with status.context(context):
            shelf, _ = self._store.create_shelf(request.shelf)
            return shelf

    def GetShelf(self, request, context):
        with status.context(context):
            return self._store.get_shelf(request.shelf)

    def DeleteShelf(self, request, context):
        with status.context(context):
            self._store.delete_shelf(request.shelf)
            return struct_pb2.Value()

    def ListBooks(self, request, context):
        with status.context(context):
            response = bookstore_pb2.ListBooksResponse()
            response.books.extend(self._store.list_books(request.shelf))
            return response

    def CreateBook(self, request, context):
        with status.context(context):
            return self._store.create_book(request.shelf, request.book)

    def GetBook(self, request, context):
        with status.context(context):
            return self._store.get_book(request.shelf, request.book)

    def DeleteBook(self, request, context):
        with status.context(context):
            self._store.delete_book(request.shelf, request.book)
            return struct_pb2.Value()


def create_sample_bookstore():
    """Creates a Bookstore with some initial sample data."""
    store = bookstore.Bookstore()

    shelf = bookstore_pb2.Shelf()
    shelf.theme = 'Fiction'
    _, fiction = store.create_shelf(shelf)

    book = bookstore_pb2.Book()
    book.title = 'README'
    book.author = "Neal Stephenson"
    store.create_book(fiction, book)

    shelf = bookstore_pb2.Shelf()
    shelf.theme = 'Fantasy'
    _, fantasy = store.create_shelf(shelf)

    book = bookstore_pb2.Book()
    book.title = 'A Game of Thrones'
    book.author = 'George R.R. Martin'
    store.create_book(fantasy, book)

    return store


def serve(port, shutdown_grace_duration):
    """Configures and runs the bookstore API server."""
    store = create_sample_bookstore()
    server = bookstore_pb2.beta_create_Bookstore_server(
        BookstoreServicer(store))
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(shutdown_grace_duration)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--port', type=int, default=8000, help='The port to listen on')
    parser.add_argument(
        '--shutdown_grace_duration', type=int, default=5,
        help='The shutdown grace duration, in seconds')

    args = parser.parse_args()

    serve(args.port, args.shutdown_grace_duration)
