# Copyright 2016 Google Inc. All rights reserved.
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

import re

from google.appengine.ext import ndb
import pytest
import webtest

import guestbook


@pytest.fixture
def app(testbed):
    return webtest.TestApp(guestbook.app)


def test_main(app):
    # Add a greeting to find
    guestbook.Greeting(
        content='Hello world',
        parent=ndb.Key('Book', 'brane3')).put()

    # Add a greeting to not find.
    guestbook.Greeting(
        content='Flat sheet',
        parent=ndb.Key('Book', 'brane2')).put()

    response = app.get('/?guestbook_name=brane3')

    assert response.status_int == 200
    assert 'Hello world' in response.body
    assert 'Flat sheet' not in response.body


def test_list(app):
    # Add greetings to find
    for i in range(11):
        guestbook.Greeting(content='Greeting {}'.format(i)).put()

    response = app.get('/list')
    assert response.status_int == 200

    assert 'Greeting 0' in response.body
    assert 'Greeting 9' in response.body
    assert 'Greeting 10' not in response.body

    next_page = re.search(r'href="([^"]+)"', response.body).group(1)
    assert next_page is not None

    response = app.get(next_page)
    assert response.status_int == 200

    assert 'Greeting 0' not in response.body
    assert 'Greeting 10' in response.body
    assert 'More' not in response.body
