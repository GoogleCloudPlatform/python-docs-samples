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

import mock
import re

from google.appengine.api import users
from google.appengine.ext import ndb
from six.moves import http_client
import pytest
import webtest

import firetactoe


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


@pytest.fixture
def app(testbed, monkeypatch, login):
    # Don't let the _get_http function memoize its value
    firetactoe._get_session.cache_clear()

    # Provide a test firebase config. The following will set the databaseURL
    # databaseURL: "http://firebase.com/test-db-url"
    monkeypatch.setattr(
        firetactoe, '_FIREBASE_CONFIG', '../firetactoe_test.py')

    login(id='38')

    firetactoe.app.debug = True
    return webtest.TestApp(firetactoe.app)


def test_index_new_game(app, monkeypatch):
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.request", autospec=True
    ) as auth_session:
        data = {'access_token': '123'}
        auth_session.return_value = MockResponse(data, http_client.OK)

        response = app.get('/')

        assert 'g=' in response.body
        # Look for the unique game token
        assert re.search(
            r'initGame[^\n]+\'[\w+/=]+\.[\w+/=]+\.[\w+/=]+\'', response.body)

        assert firetactoe.Game.query().count() == 1

        auth_session.assert_called_once_with(
            mock.ANY,  # AuthorizedSession object
            method="PATCH",
            url="http://firebase.com/test-db-url/channels/3838.json",
            body='{"winner": null, "userX": "38", "moveX": true, "winningBoard": null, "board": "         ", "userO": null}',
            data=None,
        )


def test_index_existing_game(app, monkeypatch):
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.request", autospec=True
    ) as auth_session:
        data = {'access_token': '123'}
        auth_session.return_value = MockResponse(data, http_client.OK)

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

        auth_session.assert_called_once_with(
            mock.ANY,  # AuthorizedSession object
            method="PATCH",
            url="http://firebase.com/test-db-url/channels/38razem.json",
            body='{"winner": null, "userX": "123", "moveX": null, "winningBoard": null, "board": null, "userO": "38"}',
            data=None,
        )


def test_index_nonexisting_game(app, monkeypatch):
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.request", autospec=True
    ) as auth_session:
        data = {'access_token': '123'}
        auth_session.return_value = MockResponse(data, http_client.OK)

        firetactoe.Game(id='razem', userX=users.get_current_user()).put()

        app.get('/?g=razemfrazem', status=404)

        assert not auth_session.called


def test_opened(app, monkeypatch):
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.request", autospec=True
    ) as auth_session:
        data = {'access_token': '123'}
        auth_session.return_value = MockResponse(data, http_client.OK)
        firetactoe.Game(id='razem', userX=users.get_current_user()).put()

        app.post('/opened?g=razem', status=200)

        auth_session.assert_called_once_with(
            mock.ANY,  # AuthorizedSession object
            method="PATCH",
            url="http://firebase.com/test-db-url/channels/38razem.json",
            body='{"winner": null, "userX": "38", "moveX": null, "winningBoard": null, "board": null, "userO": null}',
            data=None,
        )


def test_bad_move(app, monkeypatch):
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.request", autospec=True
    ) as auth_session:
        data = {'access_token': '123'}
        auth_session.return_value = MockResponse(data, http_client.OK)

        firetactoe.Game(
            id='razem', userX=users.get_current_user(), board=9*' ',
            moveX=True).put()

        app.post('/move?g=razem', {'i': 10}, status=400)

        assert not auth_session.called


def test_move(app, monkeypatch):
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.request", autospec=True
    ) as auth_session:
        data = {'access_token': '123'}
        auth_session.return_value = MockResponse(data, http_client.OK)

        firetactoe.Game(
            id='razem', userX=users.get_current_user(), board=9*' ',
            moveX=True).put()

        app.post('/move?g=razem', {'i': 0}, status=200)

        game = ndb.Key('Game', 'razem').get()
        assert game.board == 'X' + (8 * ' ')

        auth_session.assert_called_once_with(
            mock.ANY,  # AuthorizedSession object
            method="PATCH",
            url="http://firebase.com/test-db-url/channels/38razem.json",
            body='{"winner": null, "userX": "38", "moveX": false, "winningBoard": null, "board": "X        ", "userO": null}',
            data=None,
        )


def test_delete(app, monkeypatch):
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.request", autospec=True
    ) as auth_session:
        data = {'access_token': '123'}
        auth_session.return_value = MockResponse(data, http_client.OK)
        firetactoe.Game(id='razem', userX=users.get_current_user()).put()

        app.post('/delete?g=razem', status=200)

        auth_session.assert_called_once_with(
            mock.ANY,  # AuthorizedSession object
            method="DELETE",
            url="http://firebase.com/test-db-url/channels/38razem.json",
        )
