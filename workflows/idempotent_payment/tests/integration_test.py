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

"""Fault-injection tests that run the order workflow end to end.

These tests are skipped unless RUN_INTEGRATION_TESTS is "true". They need the
workflow (workflow.yaml), the payment function (main.py), and the stand-in
payment provider (../payment_provider) deployed, and:
    GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION (default 'us-central1'),
    WORKFLOW_ID (default 'idempotent-order-workflow'), and FIRESTORE_DATABASE.

Each test checks how many times the stand-in payment service charged.
"""

import concurrent.futures
import datetime
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
WORKFLOW_ID = os.environ.get("WORKFLOW_ID", "idempotent-order-workflow")
DATABASE = os.environ.get("FIRESTORE_DATABASE", "(default)")
AMOUNT_CENTS = 1999


@pytest.fixture(scope="module")
def db() -> firestore.Client:
    return firestore.Client(database=DATABASE)


@pytest.fixture
def order_id(db: firestore.Client) -> Iterator[str]:
    """Provides a unique order ID and deletes its test records afterward."""
    order_id = f"test-order-{uuid.uuid4().hex[:12]}"
    yield order_id
    for collection in ("orders", "payment_provider_charges", "payment_provider_faults"):
        db.collection(collection).document(order_id).delete()


def run_workflow(order_id: str) -> executions_v1.Execution:
    """Runs the workflow for an order and waits for the execution to finish."""
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
    assert execution.state == executions_v1.Execution.State.SUCCEEDED, execution.error
    return execution


def charge_record(db: firestore.Client, order_id: str) -> dict[str, Any]:
    snapshot = db.collection("payment_provider_charges").document(order_id).get()
    assert snapshot.exists, "The payment service wasn't called."
    return snapshot.to_dict()


def order_state(db: firestore.Client, order_id: str) -> str:
    return db.collection("orders").document(order_id).get().to_dict()["order_state"]


def test_duplicate_execution_charges_once(db: firestore.Client, order_id: str) -> None:
    first = json.loads(run_workflow(order_id).result)
    second = json.loads(run_workflow(order_id).result)

    assert first["already_processed"] is False
    assert second["already_processed"] is True
    assert charge_record(db, order_id)["status"] == "charged"
    assert order_state(db, order_id) == "paid"


def test_client_retry_resumes_after_partial_failure(
    db: firestore.Client, order_id: str
) -> None:
    # A previous execution created the order and then failed before payment.
    db.collection("orders").document(order_id).set(
        {"order_state": "created", "amount_cents": AMOUNT_CENTS}
    )

    run_workflow(order_id)

    assert order_state(db, order_id) == "paid"
    assert charge_record(db, order_id)["status"] == "charged"


def test_ambiguous_payment_failure_charges_once(
    db: firestore.Client, order_id: str
) -> None:
    # The payment service charges, then responds with a gateway timeout.
    db.collection("payment_provider_faults").document(order_id).set(
        {"mode": "fail_after_charge"}
    )

    run_workflow(order_id)

    record = charge_record(db, order_id)
    assert record["status"] == "charged"
    assert record["requests"] >= 2
    assert order_state(db, order_id) == "paid"


def test_timeouts_at_two_tiers_charge_once(db: firestore.Client, order_id: str) -> None:
    # The payment service charges, then responds after both the payment
    # function and the workflow stop waiting.
    db.collection("payment_provider_faults").document(order_id).set(
        {"mode": "slow_after_charge", "seconds": 45}
    )

    run_workflow(order_id)

    assert charge_record(db, order_id)["status"] == "charged"
    assert order_state(db, order_id) == "paid"


def test_crashed_attempt_is_taken_over(db: firestore.Client, order_id: str) -> None:
    # An earlier attempt claimed the payment and crashed; its claim expired.
    expired = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
        minutes=5
    )
    db.collection("orders").document(order_id).set(
        {
            "order_state": "payment_in_progress",
            "amount_cents": AMOUNT_CENTS,
            "attempt_id": "crashed-attempt",
            "lease_expires": expired,
        }
    )

    run_workflow(order_id)

    assert order_state(db, order_id) == "paid"
    assert charge_record(db, order_id)["status"] == "charged"


def test_concurrent_executions_charge_once(db: firestore.Client, order_id: str) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run_workflow, [order_id, order_id]))

    outcomes = sorted(json.loads(r.result)["already_processed"] for r in results)
    assert outcomes == [False, True]
    assert charge_record(db, order_id)["status"] == "charged"


def test_order_id_reaches_the_payment_provider(
    db: firestore.Client, order_id: str
) -> None:
    run_workflow(order_id)

    # The stand-in stores charges by Idempotency-Key, and records the order ID
    # from the request body.
    record = charge_record(db, order_id)
    assert record["order_id"] == order_id
    assert record["amount_cents"] == AMOUNT_CENTS
