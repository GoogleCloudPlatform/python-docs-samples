# Copyright 2022, Google LLC
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

"""Test webhook to enable an agent response."""

import flask
import pytest

from webhook_configure_session_parameters_enable_agent_response import (
    enable_agent_response,
)


@pytest.fixture(name="app", scope="module")
def fixture_app():
    """Flask fixture to pass a flask.Request to the test function."""
    return flask.Flask(__name__)


@pytest.mark.parametrize(
    "tag,value,expected_value",
    [
        ("increase number", 100, 200),
        ("decrease number", 100, 50),
    ],
)
def test_enable_agent_response(tag, value, expected_value, app):
    """Test for webhook to enable an agent response."""

    request = {
        "fulfillmentInfo": {"tag": tag},
        "sessionInfo": {"parameters": {"number": value}},
    }

    if tag == "increase number":
        expected_text = (
            f"The new increased value of the number parameter is {expected_value}"
        )
    else:
        expected_text = (
            f"The new decreased value of the number parameter is {expected_value}"
        )

    with app.test_request_context(json=request):
        res = enable_agent_response(flask.request)
        assert (
            res["fulfillment_response"]["messages"][0]["text"]["text"][0]
            == expected_text
        )
        assert res["sessionInfo"]["parameters"]["number"] == expected_value
