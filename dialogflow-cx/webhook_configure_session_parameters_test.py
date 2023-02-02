# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test configure new session parameters"""

import flask
import pytest

from webhook_configure_session_parameters import configure_session_params


@pytest.fixture(name="app", scope="module")
def fixture_app():
    """Flask fixture to pass a flask.Request to the test function."""
    return flask.Flask(__name__)


def test_validate_parameter(app):
    """Test for configure new session parameters."""

    request = {"fulfillmentInfo": {"tag": "configure-session-parameter"}}

    with app.test_request_context(json=request):
        res = configure_session_params(flask.request)
        assert "orderNumber" in res["sessionInfo"]["parameters"]
