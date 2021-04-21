# Copyright 2019 Google LLC All Rights Reserved.
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

import uuid

import backoff
import pytest

import quickstart


@pytest.fixture
def test_book():
    book = quickstart.Book(title=str(uuid.uuid4()))
    # The setup and teardown (put and delete) are done in separate contexts
    # only to ensure that the test phase in the middle handles contexts on its
    # own correctly. It is normally desirable to have all related sequential
    # ndb calls in the same context.
    with quickstart.client.context():
        book.put()
    yield book
    with quickstart.client.context():
        book.key.delete()


def test_quickstart(capsys, test_book):
    @backoff.on_exception(backoff.expo, AssertionError, max_time=60)
    def eventually_consistent_test():
        quickstart.list_books()
        out, _ = capsys.readouterr()
        with quickstart.client.context():
            assert test_book.title in out

    eventually_consistent_test()
