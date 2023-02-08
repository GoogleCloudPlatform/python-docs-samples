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

"""Test validate form parameter webhook snippet."""

import flask
import pytest

from webhook_prebuilt_telecom import cxPrebuiltAgentsTelecom


@pytest.fixture(name="app", scope="module")
def fixture_app():
    """Flask fixture to pass a flask.Request to the test function"""
    return flask.Flask(__name__)


def test_detect_customeranomaly_current(app):
    """Parameterized test for detecting customer anomaly webhook snippet."""

    from datetime import date

    request = {
        "fulfillmentInfo": {"tag": "detectCustomerAnomaly"},
        "pageInfo": {
            "formInfo": {
                "parameterInfo": [
                    {"displayName": "phone_number", "value": 999999},
                    {"displayName": "bill_state", "value": "current"},
                    {"displayName": "bill_amount", "value": {"amount": 1000}},
                ]
            }
        },
    }

    with app.test_request_context(json=request):
        res = cxPrebuiltAgentsTelecom(flask.request)
        assert res["sessionInfo"]["parameters"]["anomaly_detect"] == "true"
        assert res["sessionInfo"]["parameters"]["total_bill"] == 1054.34
        assert res["sessionInfo"]["parameters"]["first_month"] == str(
            date.today().replace(day=1)
        )


def test_detect_customeranomaly_other(app):
    """Parameterized test for detecting customer anomaly webhook snippet."""

    from datetime import date

    request = {
        "fulfillmentInfo": {"tag": "detectCustomerAnomaly"},
        "pageInfo": {
            "formInfo": {
                "parameterInfo": [
                    {"displayName": "phone_number", "value": 8231234789},
                    {"displayName": "bill_state", "value": "other situation"},
                    {"displayName": "bill_amount", "value": {"amount": 1000}},
                ]
            }
        },
    }

    with app.test_request_context(json=request):
        res = cxPrebuiltAgentsTelecom(flask.request)
        today = date.today()
        assert res["sessionInfo"]["parameters"]["anomaly_detect"] == "false"
        assert res["sessionInfo"]["parameters"]["total_bill"] == 1054.34
        assert res["sessionInfo"]["parameters"]["first_month"] == str(
            today.replace(day=1, month=1 + ((today.month - 2) % 12))
        )


def test_validate_phoneline(app):
    """Parameterized test for validate form parameter webhook snippet."""

    request = {
        "fulfillmentInfo": {"tag": "validatePhoneLine"},
        "pageInfo": {
            "formInfo": {
                "parameterInfo": [
                    {"displayName": "phone_number", "value": "5105105100"}
                ]
            }
        },
    }

    with app.test_request_context(json=request):
        res = cxPrebuiltAgentsTelecom(flask.request)
        assert res["sessionInfo"]["parameters"]["phone_line_verified"] == "true"


def test_invalid_phoneline(app):
    """Parameterized test for validate form parameter webhook snippet."""

    request = {
        "fulfillmentInfo": {"tag": "validatePhoneLine"},
        "pageInfo": {
            "formInfo": {
                "parameterInfo": [
                    {"displayName": "phone_number", "value": "9999999999"}
                ]
            }
        },
    }

    with app.test_request_context(json=request):
        res = cxPrebuiltAgentsTelecom(flask.request)
        assert res["sessionInfo"]["parameters"]["phone_line_verified"] == "false"


def test_invalid_phoneline2(app):
    """Parameterized test for validate form parameter webhook snippet."""

    request = {
        "fulfillmentInfo": {"tag": "validatePhoneLine"},
        "pageInfo": {
            "formInfo": {
                "parameterInfo": [
                    {"displayName": "phone_number", "value": "1231231234"}
                ]
            }
        },
    }

    with app.test_request_context(json=request):
        res = cxPrebuiltAgentsTelecom(flask.request)
        assert res["sessionInfo"]["parameters"]["domestic_coverage"] == "true"


def test_cruiseplan_coverage(app):
    """Parameterized test for cruise plan coverage webhook snippet."""

    request = {
        "fulfillmentInfo": {"tag": "cruisePlanCoverage"},
        "pageInfo": {
            "formInfo": {
                "parameterInfo": [{"displayName": "destination", "value": "mexico"}]
            }
        },
    }

    with app.test_request_context(json=request):
        res = cxPrebuiltAgentsTelecom(flask.request)
        assert res["sessionInfo"]["parameters"]["port_is_covered"] == "true"


def test_cruiseplan_notcovered(app):
    """Parameterized test for cruise plan coverage webhook snippet."""

    request = {
        "fulfillmentInfo": {"tag": "cruisePlanCoverage"},
        "pageInfo": {
            "formInfo": {
                "parameterInfo": [{"displayName": "destination", "value": "china"}]
            }
        },
    }

    with app.test_request_context(json=request):
        res = cxPrebuiltAgentsTelecom(flask.request)
        assert res["sessionInfo"]["parameters"]["port_is_covered"] == "false"


def test_international_coverage1(app):
    """Parameterized test for international coverage webhook snippet."""

    request = {
        "fulfillmentInfo": {"tag": "internationalCoverage"},
        "pageInfo": {
            "formInfo": {
                "parameterInfo": [{"displayName": "destination", "value": "singapore"}]
            }
        },
    }

    with app.test_request_context(json=request):
        res = cxPrebuiltAgentsTelecom(flask.request)
        assert res["sessionInfo"]["parameters"]["coverage"] == "both"


def test_international_coverage2(app):
    """Parameterized test for international coverage webhook snippet."""

    request = {
        "fulfillmentInfo": {"tag": "internationalCoverage"},
        "pageInfo": {
            "formInfo": {
                "parameterInfo": [{"displayName": "destination", "value": "russia"}]
            }
        },
    }

    with app.test_request_context(json=request):
        res = cxPrebuiltAgentsTelecom(flask.request)
        assert res["sessionInfo"]["parameters"]["coverage"] == "monthly_only"


def test_international_coverage3(app):
    """Parameterized test for international coverage webhook snippet."""

    request = {
        "fulfillmentInfo": {"tag": "internationalCoverage"},
        "pageInfo": {
            "formInfo": {
                "parameterInfo": [{"displayName": "destination", "value": "china"}]
            }
        },
    }

    with app.test_request_context(json=request):
        res = cxPrebuiltAgentsTelecom(flask.request)
        assert res["sessionInfo"]["parameters"]["coverage"] == "neither"


def test_cheapest_plan1(app):
    """Parameterized test for international coverage webhook snippet."""

    request = {
        "fulfillmentInfo": {"tag": "cheapestPlan"},
        "pageInfo": {
            "formInfo": {
                "parameterInfo": [{"displayName": "trip_duration", "value": 40}]
            }
        },
    }

    with app.test_request_context(json=request):
        res = cxPrebuiltAgentsTelecom(flask.request)
        assert res["sessionInfo"]["parameters"]["monthly_cost"] == 70
        assert res["sessionInfo"]["parameters"]["daily_cost"] == 400
        assert res["sessionInfo"]["parameters"]["suggested_plan"] == "monthly"


def test_cheapest_plan2(app):
    """Parameterized test for international coverage webhook snippet."""

    request = {
        "fulfillmentInfo": {"tag": "cheapestPlan"},
        "pageInfo": {
            "formInfo": {
                "parameterInfo": [{"displayName": "trip_duration", "value": 20}]
            }
        },
    }

    with app.test_request_context(json=request):
        res = cxPrebuiltAgentsTelecom(flask.request)
        assert res["sessionInfo"]["parameters"]["monthly_cost"] == 70
        assert res["sessionInfo"]["parameters"]["daily_cost"] == 200
        assert res["sessionInfo"]["parameters"]["suggested_plan"] == "monthly"


def test_cheapest_plan3(app):
    """Parameterized test for international coverage webhook snippet."""

    request = {
        "fulfillmentInfo": {"tag": "cheapestPlan"},
        "pageInfo": {
            "formInfo": {
                "parameterInfo": [{"displayName": "trip_duration", "value": 5}]
            }
        },
    }

    with app.test_request_context(json=request):
        res = cxPrebuiltAgentsTelecom(flask.request)
        assert res["sessionInfo"]["parameters"]["monthly_cost"] == 70
        assert res["sessionInfo"]["parameters"]["daily_cost"] == 50
        assert res["sessionInfo"]["parameters"]["suggested_plan"] == "daily"


def test_cheapest_plan4(app):
    """Invalid Case: This happens only when customer enters a negative number"""

    request = {
        "fulfillmentInfo": {"tag": "cheapestPlan"},
        "pageInfo": {
            "formInfo": {
                "parameterInfo": [{"displayName": "trip_duration", "value": -1}]
            }
        },
    }

    with app.test_request_context(json=request):
        res = cxPrebuiltAgentsTelecom(flask.request)
        assert res["sessionInfo"]["parameters"]["suggested_plan"] == "null"


def test_default_tag(app):
    """Default Case."""

    request = {
        "fulfillmentInfo": {"tag": None},
        "pageInfo": {
            "formInfo": {"parameterInfo": [{"displayName": None, "value": None}]}
        },
    }

    with app.test_request_context(json=request):
        res = cxPrebuiltAgentsTelecom(flask.request)
        assert res is None
