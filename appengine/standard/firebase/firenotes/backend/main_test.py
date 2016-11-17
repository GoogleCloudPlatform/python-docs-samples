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

import json

from google.appengine.ext import ndb
import jwt
import mock
import pytest


@pytest.fixture
def app():
    # Remove any existing pyjwt handlers, as firebase_helper will register
    # its own.
    try:
        jwt.unregister_algorithm('RS256')
    except KeyError:
        pass

    import main
    main.app.testing = True
    return main.app.test_client()


@pytest.fixture
def mock_token():
    patch = mock.patch('google.oauth2.id_token.verify_firebase_token')
    with patch as mock_verify:
        yield mock_verify


@pytest.fixture
def test_data():
    from main import Note
    ancestor_key = ndb.Key(Note, '123')
    notes = [
        Note(parent=ancestor_key, message='1'),
        Note(parent=ancestor_key, message='2')
    ]
    ndb.put_multi(notes)
    yield


def test_list_notes_with_mock_token(testbed, app, mock_token, test_data):
    mock_token.return_value = {'sub': '123'}

    r = app.get('/notes', headers={'Authorization': 'Bearer 123'})
    assert r.status_code == 200

    data = json.loads(r.data)
    assert len(data) == 2
    assert data[0]['message'] == '2'


def test_list_notes_with_bad_mock_token(testbed, app, mock_token):
    mock_token.return_value = None

    r = app.get('/notes', headers={'Authorization': 'Bearer 123'})
    assert r.status_code == 401


def test_add_note_with_mock_token(testbed, app, mock_token):
    mock_token.return_value = {'sub': '123'}

    r = app.post(
        '/notes',
        data=json.dumps({'message': 'Hello, world!'}),
        content_type='application/json',
        headers={'Authorization': 'Bearer 123'})

    assert r.status_code == 200

    from main import Note

    results = Note.query().fetch()
    assert len(results) == 1
    assert results[0].message == 'Hello, world!'


def test_add_note_with_bad_mock_token(testbed, app, mock_token):
    mock_token.return_value = None

    r = app.post('/notes', headers={'Authorization': 'Bearer 123'})
    assert r.status_code == 401
