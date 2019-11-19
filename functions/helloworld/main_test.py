# Copyright 2019 Google LLC
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


def test_hello_get(app):
    with app.test_request_context():
        res = main.hello_get(flask.request)
        assert 'Hello World!' in res


def test_hello_http_no_args(app):
    with app.test_request_context():
        res = main.hello_http(flask.request)
        assert 'Hello World!' in res


def test_hello_http_get(app):
    with app.test_request_context(query_string={'name': 'test'}):
        res = main.hello_http(flask.request)
        assert 'Hello test!' in res


def test_hello_http_args(app):
    with app.test_request_context(json={'name': 'test'}):
        res = main.hello_http(flask.request)
        assert 'Hello test!' in res


def test_hello_http_empty_json(app):
    with app.test_request_context(json=''):
        res = main.hello_http(flask.request)
        assert 'Hello World!' in res


def test_hello_http_xss(app):
    with app.test_request_context(json={'name': '<script>alert(1)</script>'}):
        res = main.hello_http(flask.request)
        assert '<script>' not in res


def test_hello_content_json(app):
    with app.test_request_context(json={'name': 'test'}):
        res = main.hello_content(flask.request)
        assert 'Hello test!' in res


def test_hello_content_empty_json(app):
    with app.test_request_context(json=''):
        with pytest.raises(
                ValueError,
                match="JSON is invalid, or missing a 'name' property"):
            main.hello_content(flask.request)


def test_hello_content_urlencoded(app):
    with app.test_request_context(
            data={'name': 'test'},
            content_type='application/x-www-form-urlencoded'):
        res = main.hello_content(flask.request)
        assert 'Hello test!' in res


def test_hello_content_xss(app):
    with app.test_request_context(json={'name': '<script>alert(1)</script>'}):
        res = main.hello_content(flask.request)
        assert '<script>' not in res


def test_hello_method(app):
    with app.test_request_context(method='GET'):
        res = main.hello_method(flask.request)
        assert 'Hello World!' in res
