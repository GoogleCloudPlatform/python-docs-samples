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

"""Test configure optional or required form param."""

import flask
import pytest

from webhook_configure_optional_or_required_form_parameters import (
    configure_optional_form_param,
)


@pytest.fixture(name="app", scope="module")
def fixture_app():
    """Flask fixture to pass a flask.Request to the test function."""
    return flask.Flask(__name__)


@pytest.mark.parametrize(
    "value,form_parameter,required,state,text",
    [
        (10, None, True, "INVALID", "10 isn't going to work for me. Please try again!"),
        (17, 17, False, "VALID", "17 is too many, but it's okay. Let's move on."),
        (25, None, True, "INVALID", "25 isn't going to work for me. Please try again!"),
    ],
)
def test_validate_parameter(value, form_parameter, required, state, text, app):
    """Test for configure optional or required form param."""

    request = {"pageInfo": {"formInfo": {"parameterInfo": [{"value": value}]}}}

    with app.test_request_context(json=request):
        res = configure_optional_form_param(flask.request)
        assert res["sessionInfo"]["parameterInfo"]["formParameter"] == form_parameter
        assert (
            res["pageInfo"]["formInfo"]["parameterInfo"][0]["displayName"]
            == form_parameter
        )
        assert res["pageInfo"]["formInfo"]["parameterInfo"][0]["required"] == required
        assert res["pageInfo"]["formInfo"]["parameterInfo"][0]["state"] == state
        assert res["fulfillment_response"]["messages"][0]["text"]["text"][0] == text
