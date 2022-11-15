# Copyright 2022 Google LLC
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

import unittest.mock

import flask
import pytest


@pytest.fixture(scope="module")
def app():
    """Creates a fake "app" for generating test request contexts."""
    return flask.Flask(__name__)


@unittest.mock.patch('redis.StrictRedis')
def test_visit_count(MockStrictRedis, app):
    mock_redis_client = unittest.mock.Mock()
    mock_redis_client.incr = unittest.mock.Mock(return_value=42)
    MockStrictRedis.return_value = mock_redis_client

    import main
    with app.test_request_context():
        res = main.visit_count(flask.request)
        assert 'Visit count: 42' in res
