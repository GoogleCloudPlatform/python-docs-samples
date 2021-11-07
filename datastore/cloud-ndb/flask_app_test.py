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
from google.cloud import ndb
import pytest

import flask_app


@pytest.fixture
def test_book():
    book = flask_app.Book(title=str(uuid.uuid4()))
    # The setup and teardown (put and delete) are done in separate contexts
    # only to ensure that the test phase in the middle handles contexts on its
    # own correctly. It is normally desirable to have all related sequential
    # ndb calls in the same context.
    with flask_app.client.context():
        book.put()
    yield book
    with flask_app.client.context():
        book.key.delete()


def test_index(test_book):
    flask_app.app.testing = True
    client = flask_app.app.test_client()

    @backoff.on_exception(backoff.expo, AssertionError, max_time=60)
    def eventually_consistent_test():
        r = client.get('/')
        with flask_app.client.context():
            assert r.status_code == 200
            assert test_book.title in r.data.decode('utf-8')

    eventually_consistent_test()


def test_ndb_wsgi_middleware():
    def fake_wsgi_app(environ, start_response):
        # Validate that a context is live. This will throw
        # ndb.exceptions.ContextError if no context is set up.
        ndb.context.get_context()

    wrapped_function = flask_app.ndb_wsgi_middleware(fake_wsgi_app)

    wrapped_function(None, None)
