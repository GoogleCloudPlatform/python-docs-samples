# Copyright 2023 Google LLC
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

from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch

import flask
import pytest

import main


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


def test_avoid_infinite_retries(capsys):
    now = datetime.now(timezone.utc)

    with patch("main.datetime", wraps=datetime) as datetime_mock:
        datetime_mock.now = Mock(return_value=now)

        old_event = {}
        old_event["time"] = (now - timedelta(seconds=15)).isoformat()
        old_event["id"] = "old_event_id"

        young_event = {}
        young_event["time"] = (now - timedelta(seconds=5)).isoformat()
        young_event["id"] = "young_event_id"

        main.avoid_infinite_retries(old_event)
        out, _ = capsys.readouterr()
        assert f"Dropped {old_event['id']} (age 15000.0ms)" in out

        main.avoid_infinite_retries(young_event)
        out, _ = capsys.readouterr()
        assert f"Processed {young_event['id']} (age 5000.0ms)" in out
