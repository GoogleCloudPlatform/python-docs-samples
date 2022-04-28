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

"""Test configure new session parameters trigger transition."""

import flask
import pytest

from webhook_configure_session_parameters_trigger_transition import trigger_transition


@pytest.fixture(name="app", scope="module")
def fixture_app():
    """Flask fixture to pass a flask.Request to the test function."""
    return flask.Flask(__name__)


@pytest.mark.parametrize(
    "value,expected_response",
    [
        (15, "15 is a number I can help you with!"),
        (None, "You said 25. Let me redirect you to our higher number department"),
        (30, "You said 30. Let me redirect you to our higher number department"),
    ],
)
def test_trigger_transition(value, expected_response, app):
    """Parameterized test for configure new session parameters with trigger transition."""

    if not value:
        request = {"sessionInfo": {"parameters": {}}}
    else:
        request = {"sessionInfo": {"parameters": {"value": value}}}

    with app.test_request_context(json=request):
        res = trigger_transition(flask.request)
        assert res["target_page"] == (
            "projects/<Project ID>/locations/<Location ID>/"
            "agents/<Agent ID>/flows/<Flow ID>/pages/<Page ID>"
        )
        assert (
            res["fulfillment_response"]["messages"][0]["text"]["text"][0]
            == expected_response
        )
