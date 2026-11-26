# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Fault-injection tests that run the order saga workflow end to end.

These tests are skipped unless RUN_INTEGRATION_TESTS is "true". They need the
saga workflow (workflow.yaml), the refund function (main.py), the payment
function from ../idempotent_payment, and the stand-in ../payment_provider and
../fulfillment_service deployed, and:
    GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION (default 'us-central1'),
    WORKFLOW_ID (default 'order-saga-workflow'), and FIRESTORE_DATABASE.
"""

import json
import os
import time
from typing import Any, Iterator
import uuid

from google.cloud import firestore
from google.cloud.workflows import executions_v1
import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_INTEGRATION_TESTS") != "true",
    reason="Set RUN_INTEGRATION_TESTS=true to run integration tests.",
)

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
LOCATION_ID = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
WORKFLOW_ID = os.environ.get("WORKFLOW_ID", "order-saga-workflow")
DATABASE = os.environ.get("FIRESTORE_DATABASE", "(default)")
AMOUNT_CENTS = 4999


@pytest.fixture(scope="module")
def db() -> firestore.Client:
    return firestore.Client(database=DATABASE)


@pytest.fixture
def order_id(db: firestore.Client) -> Iterator[str]:
    """Provides a unique order ID and deletes its test records afterward."""
    order_id = f"test-order-{uuid.uuid4().hex[:12]}"
    yield order_id
    for collection in (
        "orders",
        "fulfillment_service_faults",
        "payment_provider_charges",
        "payment_provider_faults",
    ):
        db.collection(collection).document(order_id).delete()
    db.collection("payment_provider_faults").document(f"refund-{order_id}").delete()


def run_saga(order_id: str) -> executions_v1.Execution:
    """Runs the saga for an order and waits for the execution to finish."""
    client = executions_v1.ExecutionsClient()
    parent = f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/workflows/{WORKFLOW_ID}"
    argument = json.dumps({"order_id": order_id, "amount_cents": AMOUNT_CENTS})
    execution = client.create_execution(
        parent=parent, execution=executions_v1.Execution(argument=argument)
    )
    deadline = time.monotonic() + 600
    while execution.state == executions_v1.Execution.State.ACTIVE:
        assert time.monotonic() < deadline, "The execution didn't finish."
        time.sleep(3)
        execution = client.get_execution(name=execution.name)
    return execution


def ledger(db: firestore.Client, key: str) -> dict[str, Any] | None:
    """Returns the stand-in payment provider's record for a key, if any."""
    snapshot = db.collection("payment_provider_charges").document(key).get()
    return snapshot.to_dict() if snapshot.exists else None


def order_state(db: firestore.Client, order_id: str) -> str:
    return db.collection("orders").document(order_id).get().to_dict()["order_state"]


def test_fulfilled_order_is_not_refunded(db: firestore.Client, order_id: str) -> None:
    execution = run_saga(order_id)

    assert json.loads(execution.result)["status"] == "fulfilled"
    assert ledger(db, order_id)["status"] == "charged"


def test_failed_fulfillment_refunds_once(db: firestore.Client, order_id: str) -> None:
    db.collection("fulfillment_service_faults").document(order_id).set({"mode": "fail"})

    execution = run_saga(order_id)

    assert json.loads(execution.result)["status"] == "refunded"
    record = ledger(db, order_id)
    assert record["status"] == "refunded"
    assert record["refund_requests"] == 1
    assert order_state(db, order_id) == "refunded"


def test_exhausted_charge_retries_compensate_silent_charge(
    db: firestore.Client, order_id: str
) -> None:
    # First call charges and responds 504; every retry also responds 504 until
    # http.default_retry (5 attempts) gives up. Compensation must undo the charge.
    db.collection("payment_provider_faults").document(order_id).set(
        {"mode": "fail_after_charge", "remaining": 10}
    )

    execution = run_saga(order_id)

    assert execution.state == executions_v1.Execution.State.SUCCEEDED
    assert json.loads(execution.result)["status"] == "refunded"
    assert ledger(db, order_id)["status"] == "refunded"
    assert order_state(db, order_id) == "refunded"


def test_retried_compensation_refunds_once(db: firestore.Client, order_id: str) -> None:
    db.collection("fulfillment_service_faults").document(order_id).set({"mode": "fail"})
    # The provider refunds, then responds with a gateway timeout once.
    db.collection("payment_provider_faults").document(f"refund-{order_id}").set(
        {"mode": "fail_after_charge"}
    )

    execution = run_saga(order_id)

    assert json.loads(execution.result)["status"] == "refunded"
    record = ledger(db, order_id)
    assert record["status"] == "refunded"
    assert record["refund_requests"] >= 2


def test_retrying_a_refunded_order_moves_no_money(
    db: firestore.Client, order_id: str
) -> None:
    db.collection("fulfillment_service_faults").document(order_id).set({"mode": "fail"})
    run_saga(order_id)

    # The client retries the same order after it was refunded. The payment
    # function returns 409 for a final state, and compensation is idempotent.
    execution = run_saga(order_id)

    assert execution.state == executions_v1.Execution.State.SUCCEEDED
    assert json.loads(execution.result)["status"] == "refunded"
    assert ledger(db, order_id)["status"] == "refunded"
    assert order_state(db, order_id) == "refunded"
