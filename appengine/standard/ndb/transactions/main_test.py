# Copyright 2015 Google Inc. All rights reserved.
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

import main


@pytest.fixture
def app(testbed):
    main.app.config['TESTING'] = True
    return main.app.test_client()


def test_index(app):
    rv = app.get('/')
    assert 'Permanent note page' in rv.data
    assert rv.status == '200 OK'


def test_post(app):
    rv = app.post('/add', data=dict(
        note_title='Title',
        note_text='Text'
    ), follow_redirects=True)
    assert rv.status == '200 OK'


def test_there(app):
    rv = app.post('/add', data=dict(
        note_title='Title',
        note_text='New'
    ), follow_redirects=True)
    rv = app.post('/add', data=dict(
        note_title='Title',
        note_text='There'
    ), follow_redirects=True)
    assert 'Already there' in rv.data
    assert rv.status == '200 OK'
