# Copyright 2019 Google LLC
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

# [START datastore_quickstart_python]
from google.cloud import ndb


class Book(ndb.Model):
    title = ndb.StringProperty()


client = ndb.Client()


def list_books():
    with client.context():
        books = Book.query()
        for book in books:
            print(book.to_dict())
# [END datastore_quickstart_python]


if __name__ == "__main__":
    list_books()
