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

# With a real payment provider, replace the ID token with the provider's own
# credentials, such as an API key in Secret Manager. Keep the Idempotency-Key.

# [START workflows_idempotent_process_payment]
import datetime
import os
import uuid

import flask
import functions_framework
from google.api_core import exceptions
from google.auth.transport.requests import Request
from google.cloud import firestore
from google.oauth2 import id_token
import requests

# Longer than a payment takes, so only a crashed attempt's claim expires.
LEASE = datetime.timedelta(minutes=2)
# The payment provider's base URL. Required: the function fails to start without it.
PAYMENT_PROVIDER_URL = os.environ["PAYMENT_PROVIDER_URL"]
# Later states, such as refunded, are final: retrying the order doesn't charge again.
CHARGEABLE_STATES = ("created", "payment_failed", "payment_in_progress")
# Errors that can succeed on retry. Firestore raises a ValueError caused by
# Aborted when a transaction runs out of attempts under contention.
TEMPORARY_ERRORS = (
    exceptions.Aborted,
    exceptions.DeadlineExceeded,
    exceptions.InternalServerError,
    exceptions.ServiceUnavailable,
    exceptions.TooManyRequests,
)

db = firestore.Client(database=os.environ.get("FIRESTORE_DATABASE", "(default)"))


def is_temporary(err: Exception) -> bool:
    """Returns True if the error, or the error that caused it, is temporary."""
    cause = err.__cause__ or err.__context__
    return isinstance(err, TEMPORARY_ERRORS) or isinstance(cause, TEMPORARY_ERRORS)


def payment_status(order: dict | None, now: datetime.datetime) -> str:
    """Returns what to do with the order: charge it, or why not."""
    if order is None:
        return "missing"
    if order["order_state"] == "paid":
        return "paid"
    if order["order_state"] == "payment_in_progress" and order["lease_expires"] > now:
        return "in_progress"
    if order["order_state"] not in CHARGEABLE_STATES:
        return "final"
    return "chargeable"


@firestore.transactional
def claim_payment(
    transaction: firestore.Transaction,
    order_ref: firestore.DocumentReference,
    attempt_id: str,
    now: datetime.datetime,
) -> tuple[str, int]:
    """Claims the order's payment unless it's paid or another attempt holds it.

    Returns the order's status and amount.
    """
    order = order_ref.get(transaction=transaction).to_dict()
    status = payment_status(order, now)
    if status == "chargeable":
        transaction.update(
            order_ref,
            {
                "order_state": "payment_in_progress",
                "attempt_id": attempt_id,
                "lease_expires": now + LEASE,
            },
        )
        status = "claimed"
    return status, (order or {}).get("amount_cents", 0)


@firestore.transactional
def finish_payment(
    transaction: firestore.Transaction,
    order_ref: firestore.DocumentReference,
    attempt_id: str,
    order_state: str,
) -> None:
    """Records the result, if this attempt still holds the claim."""
    snapshot = order_ref.get(transaction=transaction)
    if snapshot.exists and snapshot.to_dict().get("attempt_id") == attempt_id:
        transaction.update(order_ref, {"order_state": order_state})


def charge(order_id: str, amount_cents: int) -> None:
    """Charges the order through the payment provider, at most once per order ID."""
    token = id_token.fetch_id_token(Request(), PAYMENT_PROVIDER_URL)
    response = requests.post(
        f"{PAYMENT_PROVIDER_URL}/charges",
        json={"order_id": order_id, "amount_cents": amount_cents},
        # The provider charges each idempotency key only once, so a retry
        # after an ambiguous failure can't charge the customer twice.
        headers={"Authorization": f"Bearer {token}", "Idempotency-Key": order_id},
        timeout=30,
    )
    response.raise_for_status()


def pay(order_id: str) -> tuple[dict, int]:
    """Charges the order unless it's already paid, final, or in progress."""
    order_ref = db.collection("orders").document(order_id)
    attempt_id = uuid.uuid4().hex
    now = datetime.datetime.now(datetime.timezone.utc)

    # Most retries find the order paid or in progress. Checking with a plain
    # read first keeps them out of transactions on this order's document.
    status = payment_status(order_ref.get().to_dict(), now)
    amount_cents = 0
    if status == "chargeable":
        status, amount_cents = claim_payment(
            db.transaction(), order_ref, attempt_id, now
        )
    if status == "missing":
        return {"error": f"order {order_id} not found"}, 404
    if status == "paid":
        return {"order_id": order_id, "status": "paid", "already_processed": True}, 200
    if status == "in_progress":
        # The workflow's retry policy retries 503 responses after a backoff.
        return {"error": "payment in progress"}, 503
    if status == "final":
        return {"error": f"order {order_id} can't be charged again"}, 409

    # Charge outside the transaction: Firestore can rerun a transaction, but it
    # can't undo a call to another service.
    try:
        charge(order_id, amount_cents)
    except requests.RequestException as err:
        finish_payment(db.transaction(), order_ref, attempt_id, "payment_failed")
        return {"error": f"payment failed: {err}"}, 503
    finish_payment(db.transaction(), order_ref, attempt_id, "paid")
    return {"order_id": order_id, "status": "paid", "already_processed": False}, 200


@functions_framework.http
def process_payment(request: flask.Request) -> tuple[dict, int]:
    """Processes an order's payment once, even when the workflow retries the call."""
    order_id = (request.get_json(silent=True) or {}).get("order_id")
    if not order_id:
        return {"error": "missing order_id"}, 400
    try:
        return pay(str(order_id))
    except Exception as err:
        if is_temporary(err):
            # Contention or a brief outage: let the workflow retry.
            return {"error": f"temporary error: {err}"}, 503
        raise  # A permanent error, such as missing permissions: fail with 500.


# [END workflows_idempotent_process_payment]
