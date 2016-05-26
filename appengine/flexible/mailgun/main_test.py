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

import os

import pytest
import requests
import responses


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv('MAILGUN_DOMAIN_NAME', 'example.com')
    monkeypatch.setenv('MAILGUN_API_KEY', 'apikey')

    import main

    main.app.testing = True
    return main.app.test_client()


def test_index(app):
    r = app.get('/')
    assert r.status_code == 200


@responses.activate
def test_send_error(app):
    responses.add(
        responses.POST,
        'https://api.mailgun.net/v3/example.com/messages',
        body='Test error',
        status=500)

    with pytest.raises(requests.exceptions.HTTPError):
        app.post('/send/email', data={
            'recipient': 'user@example.com',
            'submit': 'Send simple email'})


@responses.activate
def test_send_simple(app):
    responses.add(
        responses.POST,
        'https://api.mailgun.net/v3/example.com/messages',
        body='')

    response = app.post('/send/email', data={
        'recipient': 'user@example.com',
        'submit': 'Send simple email'})
    assert response.status_code == 200
    assert len(responses.calls) == 1


@responses.activate
def test_send_complex(app, monkeypatch):
    import main
    monkeypatch.chdir(os.path.dirname(main.__file__))

    responses.add(
        responses.POST,
        'https://api.mailgun.net/v3/example.com/messages',
        body='')

    response = app.post('/send/email', data={
        'recipient': 'user@example.com',
        'submit': 'Send complex email'})
    assert response.status_code == 200
    assert len(responses.calls) == 1
