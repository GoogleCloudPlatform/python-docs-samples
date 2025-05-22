# Copyright 2025 Google LLC
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

from cloudevents.conversion import to_structured
from cloudevents.http import CloudEvent

from flask.testing import FlaskClient

from functions_framework import create_app

import pytest


@pytest.fixture
def cloud_event_budget_alert() -> CloudEvent:
    attributes = {
        "specversion": "1.0",
        "id": "my-id",
        "source": "//pubsub.googleapis.com/projects/PROJECT_NAME/topics/TOPIC_NAME",
        "type": "google.cloud.pubsub.topic.v1.messagePublished",
        "datacontenttype": "application/json",
        "time": "2025-05-09T18:32:46.572Z"
    }

    budget_data = {
        "budgetDisplayName": "BUDGET_NAME",
        "alertThresholdExceeded": 1.0,
        "costAmount": 2.0,
        "costIntervalStart": "2025-05-01T07:00:00Z",
        "budgetAmount": 0.01,
        "budgetAmountType": "SPECIFIED_AMOUNT",
        "currencyCode": "USD"
    }

    json_string = json.dumps(budget_data)
    message_base64 = base64.b64encode(json_string.encode('utf-8')).decode('utf-8')

    data = {
        "message": {
            "data": message_base64
        }
    }

    return CloudEvent(attributes, data)


@pytest.fixture
def client() -> FlaskClient:
    source = "stop_billing.py"
    target = "stop_billing"
    return create_app(target, source, "cloudevent").test_client()


def test_receive_notification_to_stop_billing(
    client: FlaskClient,
    cloud_event_budget_alert: CloudEvent,
    capsys: pytest.CaptureFixture[str]
) -> None:
    headers, data = to_structured(cloud_event_budget_alert)
    resp = client.post("/", headers=headers, data=data)

    captured = capsys.readouterr()

    assert resp.status_code == 200
    assert resp.data == b"OK"

    assert "Getting billing info for project" in captured.out
    assert "Disabling billing for project" in captured.out
    assert "Billing disabled. (Simulated)" in captured.out
