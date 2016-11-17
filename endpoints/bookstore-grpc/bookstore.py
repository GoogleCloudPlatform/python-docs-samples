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

import threading

import status


class ShelfInfo(object):
  """The contents of a single shelf."""
  def __init__(self, shelf):
    self._shelf = shelf
    self._last_book_id = 0
    self._books = Bookstore.BookDict()

class Bookstore(object):
  """An in-memory backend for storing Bookstore data."""

  class ShelfDict(dict):
    def __missing__(self, key):
      raise status.StatusException(status.Code.NOT_FOUND,
                                   'Unable to find shelf "%s"' % key)

  class BookDict(dict):
    def __missing__(self, key):
      raise status.StatusException(status.Code.NOT_FOUND,
                                   'Unable to find book "%s"' % key)

  def __init__(self):
    self._last_shelf_id = 0
    self._shelves = Bookstore.ShelfDict()
    self._lock = threading.Lock()

  def list_shelf(self):
    with self._lock:
      return [s._shelf for (_, s) in self._shelves.iteritems()]

  def create_shelf(self, shelf):
    with self._lock:
      self._last_shelf_id += 1
      shelf_id = self._last_shelf_id
      shelf.id = shelf_id
      self._shelves[shelf_id] = ShelfInfo(shelf)
      return (shelf, shelf_id)

  def get_shelf(self, shelf_id):
    with self._lock:
      return self._shelves[shelf_id]._shelf

  def delete_shelf(self, shelf_id):
    with self._lock:
      _ = self._shelves[shelf_id]
      del self._shelves[shelf_id]

  def list_books(self, shelf_id):
    with self._lock:
      return [book for (_, book) in self._shelves[shelf_id]._books.iteritems()]

  def create_book(self, shelf_id, book):
    with self._lock:
      shelf_info = self._shelves[shelf_id]
      shelf_info._last_book_id += 1
      book_id = shelf_info._last_book_id
      book.id = book_id
      shelf_info._books[book_id] = book
      return book

  def get_book(self, shelf_id, book_id):
    with self._lock:
      return self._shelves[shelf_id]._books[book_id]

  def delete_book(self, shelf_id, book_id):
    with self._lock:
      _ = self._shelves[shelf_id]._books[book_id]
      del self._shelves[shelf_id]._books[book_id]
