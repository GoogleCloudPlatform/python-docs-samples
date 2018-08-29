# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import flask
import pytest

import main


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


def test_cors_enabled_function_preflight(app):
    with app.test_request_context(method='OPTIONS'):
        res = main.cors_enabled_function(flask.request)
        assert res[2].get('Access-Control-Allow-Origin') == '*'
        assert res[2].get('Access-Control-Allow-Methods') == 'GET'
        assert res[2].get('Access-Control-Allow-Headers') == 'Content-Type'
        assert res[2].get('Access-Control-Max-Age') == '3600'


def test_cors_enabled_function_main(app):
    with app.test_request_context(method='GET'):
        res = main.cors_enabled_function(flask.request)
        assert res[2].get('Access-Control-Allow-Origin') == '*'


def test_cors_enabled_function_auth_preflight(app):
    with app.test_request_context(method='OPTIONS'):
        res = main.cors_enabled_function_auth(flask.request)
        assert res[2].get('Access-Control-Allow-Origin') == \
            'https://mydomain.com'
        assert res[2].get('Access-Control-Allow-Methods') == 'GET'
        assert res[2].get('Access-Control-Allow-Headers') == 'Authorization'
        assert res[2].get('Access-Control-Max-Age') == '3600'
        assert res[2].get('Access-Control-Allow-Credentials') == 'true'


def test_cors_enabled_function_auth_main(app):
    with app.test_request_context(method='GET'):
        res = main.cors_enabled_function_auth(flask.request)
        assert res[2].get('Access-Control-Allow-Origin') == \
            'https://mydomain.com'
        assert res[2].get('Access-Control-Allow-Credentials') == 'true'
