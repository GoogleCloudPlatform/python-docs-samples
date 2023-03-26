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

import base64
import json
from unittest.mock import MagicMock, Mock, patch

import flask
import pytest

import main


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


def test_retry_or_not():
    with patch("main.error_client") as error_client_mock:
        error_client_mock.report_exception = MagicMock()

        event = Mock(data={})

        try_again = {"retry": True}
        dont_try_again = {"retry": False}

        event.data = {
            "message": {
                "data": base64.b64encode(json.dumps(dont_try_again).encode("utf-8"))
            }
        }
        main.retry_or_not(event)
        assert error_client_mock.report_exception.call_count == 1

        event.data = {
            "message": {"data": base64.b64encode(json.dumps(try_again).encode("utf-8"))}
        }
        with pytest.raises(RuntimeError):
            main.retry_or_not(event)

        assert error_client_mock.report_exception.call_count == 2
