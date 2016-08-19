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
import pytest
import webtest

import xmpp


@pytest.fixture
def app(testbed):
    return webtest.TestApp(xmpp.app)


@mock.patch('xmpp.xmpp')
def test_chat(xmpp_mock, app):
    app.post('/_ah/xmpp/message/chat/', {
        'from': 'sender@example.com',
        'to': 'recipient@example.com',
        'body': 'hello',
    })


@mock.patch('xmpp.xmpp')
def test_subscribe(xmpp_mock, app):
    app.post('/_ah/xmpp/subscribe')


@mock.patch('xmpp.xmpp')
def test_check_presence(xmpp_mock, app):

    app.post('/_ah/xmpp/presence/available', {
        'from': 'sender@example.com'
    })


@mock.patch('xmpp.xmpp')
def test_send_presence(xmpp_mock, app):
    app.post('/send_presence', {
        'jid': 'node@domain/resource'
    })


@mock.patch('xmpp.xmpp')
def test_error(xmpp_mock, app):
    app.post('/_ah/xmpp/error/', {
        'from': 'sender@example.com',
        'stanza': 'hello world'
    })


@mock.patch('xmpp.xmpp')
def test_send_chat(xmpp_mock, app):
    app.post('/send_chat')
