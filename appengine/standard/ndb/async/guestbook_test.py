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

import pytest
import webtest

import guestbook


@pytest.fixture
def app(testbed):
    return webtest.TestApp(guestbook.app)


def test_get_guestbook_sync(app, testbed, login):
    guestbook.Account(id='123').put()
    # Log the user in
    login(id='123')

    for i in range(11):
        guestbook.Guestbook(content='Content {}'.format(i)).put()

    response = app.get('/guestbook')

    assert response.status_int == 200
    assert 'Content 1' in response.body


def test_get_guestbook_async(app, testbed, login):
    guestbook.Account(id='123').put()
    # Log the user in
    login(id='123')
    for i in range(11):
        guestbook.Guestbook(content='Content {}'.format(i)).put()

    response = app.get('/guestbook?async=1')

    assert response.status_int == 200
    assert 'Content 1' in response.body


def test_get_messages_sync(app, testbed):
    for i in range(21):
        account_key = guestbook.Account(nickname='Nick {}'.format(i)).put()
        guestbook.Message(author=account_key, text='Text {}'.format(i)).put()

    response = app.get('/messages')

    assert response.status_int == 200
    assert 'Nick 1 wrote:' in response.body
    assert '<p>Text 1' in response.body


def test_get_messages_async(app, testbed):
    for i in range(21):
        account_key = guestbook.Account(nickname='Nick {}'.format(i)).put()
        guestbook.Message(author=account_key, text='Text {}'.format(i)).put()

    response = app.get('/messages?async=1')

    assert response.status_int == 200
    assert 'Nick 1 wrote:' in response.body
    assert '\nText 1' in response.body
