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

from collections import UserDict
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, Mock, patch

import flask
import pytest
import requests
import responses

import main


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


def test_lazy_globals(app):
    with app.test_request_context():
        main.lazy_globals(flask.request)


def test_scope_demo(app):
    with app.test_request_context():
        res = main.scope_demo(flask.request)
        assert res == 'Per instance: 362880, per function: 45'


@responses.activate
def test_connection_pooling_200(app):
    responses.add(responses.GET, 'http://example.com',
                  json={'status': 'OK'}, status=200)
    with app.test_request_context():
        main.connection_pooling(flask.request)


@responses.activate
def test_connection_pooling_404(app):
    responses.add(responses.GET, 'http://example.com',
                  json={'error': 'not found'}, status=404)
    with app.test_request_context():
        with pytest.raises(requests.exceptions.HTTPError):
            main.connection_pooling(flask.request)


def test_avoid_infinite_retries(capsys):
    now = datetime.now(timezone.utc)

    with patch('main.datetime', wraps=datetime) as datetime_mock:
        datetime_mock.now = Mock(return_value=now)

        old_context = UserDict()
        old_context.timestamp = (now - timedelta(seconds=15)).isoformat()
        old_context.event_id = 'old_event_id'

        young_context = UserDict()
        young_context.timestamp = (now - timedelta(seconds=5)).isoformat()
        young_context.event_id = 'young_event_id'

        main.avoid_infinite_retries(None, old_context)
        out, _ = capsys.readouterr()
        assert f"Dropped {old_context.event_id} (age 15000.0ms)" in out

        main.avoid_infinite_retries(None, young_context)
        out, _ = capsys.readouterr()
        assert f"Processed {young_context.event_id} (age 5000.0ms)" in out


def test_retry_or_not():
    with patch('main.error_client') as error_client_mock:
        error_client_mock.report_exception = MagicMock()

        event = Mock(data={})
        main.retry_or_not(event, None)
        assert error_client_mock.report_exception.call_count == 1

        event.data = {'retry': True}
        with pytest.raises(RuntimeError):
            main.retry_or_not(event, None)

        assert error_client_mock.report_exception.call_count == 2
