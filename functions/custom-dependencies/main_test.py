# Copyright 2021 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# NOTE:
# To pass these tests locally, run `brew install graphviz`


from unittest.mock import Mock
import pytest
import flask

import main


@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


def test_empty_query_string(app):
    with app.test_request_context():
        req = Mock(args={})
        res = main.http_handler(req)
        assert res.status_code == 400


def test_empty_dot_parameter(app):
    with app.test_request_context():
        req = Mock(args={"dot": ""})
        res = main.http_handler(req)
        assert res.status_code == 400


def test_bad_dot_parameter(app):
    with app.test_request_context():
        req = Mock(args={"dot": "digraph"})
        res = main.http_handler(req)
        assert res.status_code == 400


def test_good_dot_parameter(app):
    with app.test_request_context():
        req = Mock(args={"dot": "digraph G { A -> {B, C, D} -> {F} }"})
        res = main.http_handler(req)
        assert res.headers["Content-Type"] == "image/png"
