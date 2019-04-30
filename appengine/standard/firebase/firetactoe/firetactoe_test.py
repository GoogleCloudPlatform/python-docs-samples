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

import json
import re

from google.appengine.api import users
from google.appengine.ext import ndb
import httplib2
import pytest
import webtest

import firetactoe


class MockHttp(object):
    """Mock the Http object, so we can set what the response will be."""
    def __init__(self, status, content=''):
        self.content = content
        self.status = status
        self.request_url = None

    def __call__(self, *args, **kwargs):
        return self

    def request(self, url, method, content='', *args, **kwargs):
        self.request_url = url
        self.request_method = method
        self.request_content = content
        return self, self.content


@pytest.fixture
def app(testbed, monkeypatch, login):
    # Don't let the _get_http function memoize its value
    firetactoe._get_http.cache_clear()

    # Provide a test firebase config. The following will set the databaseURL
    # databaseURL: "http://firebase.com/test-db-url"
    monkeypatch.setattr(
        firetactoe, '_FIREBASE_CONFIG', '../firetactoe_test.py')

    login(id='38')

    firetactoe.app.debug = True
    return webtest.TestApp(firetactoe.app)


def test_index_new_game(app, monkeypatch):
    mock_http = MockHttp(200, content=json.dumps({'access_token': '123'}))
    monkeypatch.setattr(httplib2, 'Http', mock_http)

    response = app.get('/')

    assert 'g=' in response.body
    # Look for the unique game token
    assert re.search(
        r'initGame[^\n]+\'[\w+/=]+\.[\w+/=]+\.[\w+/=]+\'', response.body)

    assert firetactoe.Game.query().count() == 1

    assert mock_http.request_url.startswith(
        'http://firebase.com/test-db-url/channels/')
    assert mock_http.request_method == 'PATCH'


def test_index_existing_game(app, monkeypatch):
    mock_http = MockHttp(200, content=json.dumps({'access_token': '123'}))
    monkeypatch.setattr(httplib2, 'Http', mock_http)
    userX = users.User('x@example.com', _user_id='123')
    firetactoe.Game(id='razem', userX=userX).put()

    response = app.get('/?g=razem')

    assert 'g=' in response.body
    # Look for the unique game token
    assert re.search(
        r'initGame[^\n]+\'[\w+/=]+\.[\w+/=]+\.[\w+/=]+\'', response.body)

    assert firetactoe.Game.query().count() == 1
    game = ndb.Key('Game', 'razem').get()
    assert game is not None
    assert game.userO.user_id() == '38'

    assert mock_http.request_url.startswith(
        'http://firebase.com/test-db-url/channels/')
    assert mock_http.request_method == 'PATCH'


def test_index_nonexisting_game(app, monkeypatch):
    mock_http = MockHttp(200, content=json.dumps({'access_token': '123'}))
    monkeypatch.setattr(httplib2, 'Http', mock_http)
    firetactoe.Game(id='razem', userX=users.get_current_user()).put()

    app.get('/?g=razemfrazem', status=404)

    assert mock_http.request_url is None


def test_opened(app, monkeypatch):
    mock_http = MockHttp(200, content=json.dumps({'access_token': '123'}))
    monkeypatch.setattr(httplib2, 'Http', mock_http)
    firetactoe.Game(id='razem', userX=users.get_current_user()).put()

    app.post('/opened?g=razem', status=200)

    assert mock_http.request_url.startswith(
        'http://firebase.com/test-db-url/channels/')
    assert mock_http.request_method == 'PATCH'


def test_bad_move(app, monkeypatch):
    mock_http = MockHttp(200, content=json.dumps({'access_token': '123'}))
    monkeypatch.setattr(httplib2, 'Http', mock_http)
    firetactoe.Game(
        id='razem', userX=users.get_current_user(), board=9*' ',
        moveX=True).put()

    app.post('/move?g=razem', {'i': 10}, status=400)

    assert mock_http.request_url is None


def test_move(app, monkeypatch):
    mock_http = MockHttp(200, content=json.dumps({'access_token': '123'}))
    monkeypatch.setattr(httplib2, 'Http', mock_http)
    firetactoe.Game(
        id='razem', userX=users.get_current_user(), board=9*' ',
        moveX=True).put()

    app.post('/move?g=razem', {'i': 0}, status=200)

    game = ndb.Key('Game', 'razem').get()
    assert game.board == 'X' + (8 * ' ')

    assert mock_http.request_url.startswith(
        'http://firebase.com/test-db-url/channels/')
    assert mock_http.request_method == 'PATCH'


def test_delete(app, monkeypatch):
    mock_http = MockHttp(200, content=json.dumps({'access_token': '123'}))
    monkeypatch.setattr(httplib2, 'Http', mock_http)
    firetactoe.Game(id='razem', userX=users.get_current_user()).put()

    app.post('/delete?g=razem', status=200)

    assert mock_http.request_url.startswith(
        'http://firebase.com/test-db-url/channels/')
    assert mock_http.request_method == 'DELETE'
