# Copyright 2021, Google LLC
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

"""Test webhook"""

import flask
import pytest

from webhook_validate_form_parameter import validate_parameter


@pytest.fixture(name="app", scope="module")
def fixture_app():
    """Flask fixture to pass a flask.Request to the test function"""
    return flask.Flask(__name__)


@pytest.mark.parametrize(
    "value,expected_response",
    [
        (15, "That is a number I can work with!"),
        (16, "That is too many! Please pick another number."),
    ],
)
def test_validate_parameter(value, expected_response, app):
    """Parameterized test for validate form parameter webhook snippet."""

    request = {"pageInfo": {"formInfo": {"parameterInfo": [{"value": value}]}}}

    with app.test_request_context(json=request):
        res = validate_parameter(flask.request)
        assert (
            res["fulfillment_response"]["messages"][0]["text"]["text"][0]
            == expected_response
        )
