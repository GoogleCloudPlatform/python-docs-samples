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
# credentials, such as an API key in Secret Manager.

# [START workflows_order_saga_refund]
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

# Longer than a refund takes, so only a crashed attempt's claim expires.
LEASE = datetime.timedelta(minutes=2)
# The payment provider's base URL. Required: the function fails to start without it.
PAYMENT_PROVIDER_URL = os.environ["PAYMENT_PROVIDER_URL"]
# Orders that might have been charged. A payment that's still in progress with
# an active lease is excluded: the caller waits for it instead.
REFUNDABLE_STATES = (
    "paid",
    "payment_failed",
    "payment_in_progress",
    "refund_failed",
    "refund_in_progress",
)
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


def refund_status(order: dict | None, now: datetime.datetime) -> str:
    """Returns what to do with the order: refund or cancel it, or why not."""
    if order is None:
        return "missing"
    state = order["order_state"]
    if state in ("refunded", "cancelled"):
        return state
    if state in ("payment_in_progress", "refund_in_progress") and (
        order["lease_expires"] > now
    ):
        return "in_progress"
    if state == "created":
        return "cancellable"  # Never charged, so there's nothing to refund.
    if state in REFUNDABLE_STATES:
        return "refundable"
    return "final"


@firestore.transactional
def claim_refund(
    transaction: firestore.Transaction,
    order_ref: firestore.DocumentReference,
    attempt_id: str,
    now: datetime.datetime,
) -> str:
    """Claims the order's refund, or cancels an order that was never charged."""
    status = refund_status(order_ref.get(transaction=transaction).to_dict(), now)
    if status == "cancellable":
        transaction.update(order_ref, {"order_state": "cancelled"})
        return "cancelled_now"
    if status == "refundable":
        transaction.update(
            order_ref,
            {
                "order_state": "refund_in_progress",
                "attempt_id": attempt_id,
                "lease_expires": now + LEASE,
            },
        )
        return "claimed"
    return status


@firestore.transactional
def finish_refund(
    transaction: firestore.Transaction,
    order_ref: firestore.DocumentReference,
    attempt_id: str,
    order_state: str,
) -> None:
    """Records the result, if this attempt still holds the claim."""
    snapshot = order_ref.get(transaction=transaction)
    if snapshot.exists and snapshot.to_dict().get("attempt_id") == attempt_id:
        transaction.update(order_ref, {"order_state": order_state})


def refund(order_id: str) -> bool:
    """Refunds the order's charge, if any. Returns True if money was refunded.

    The provider keys refunds by the charge, so repeating a refund has no
    effect, and a charge that arrives after the refund is rejected.
    """
    token = id_token.fetch_id_token(Request(), PAYMENT_PROVIDER_URL)
    response = requests.post(
        f"{PAYMENT_PROVIDER_URL}/refunds",
        json={"charge_key": order_id},
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["refunded"]


def compensate(order_id: str) -> tuple[dict, int]:
    """Refunds or cancels the order once, whether or not it was charged."""
    order_ref = db.collection("orders").document(order_id)
    attempt_id = uuid.uuid4().hex
    now = datetime.datetime.now(datetime.timezone.utc)

    # Checking with a plain read first keeps retries for finished orders out
    # of transactions on this order's document.
    status = refund_status(order_ref.get().to_dict(), now)
    if status in ("cancellable", "refundable"):
        status = claim_refund(db.transaction(), order_ref, attempt_id, now)
    if status == "missing":
        return {"error": f"order {order_id} not found"}, 404
    if status in ("refunded", "cancelled"):
        return {"order_id": order_id, "status": status, "already_processed": True}, 200
    if status == "cancelled_now":
        return {
            "order_id": order_id,
            "status": "cancelled",
            "already_processed": False,
        }, 200
    if status == "in_progress":
        # The workflow's retry policy retries 503 responses after a backoff.
        return {"error": "payment or refund in progress"}, 503
    if status == "final":
        return {"error": f"order {order_id} can't be refunded"}, 409

    # Refund outside the transaction: Firestore can rerun a transaction, but it
    # can't undo a call to another service.
    try:
        refunded = refund(order_id)
    except requests.RequestException as err:
        finish_refund(db.transaction(), order_ref, attempt_id, "refund_failed")
        return {"error": f"refund failed: {err}"}, 503
    order_state = "refunded" if refunded else "cancelled"
    finish_refund(db.transaction(), order_ref, attempt_id, order_state)
    return {
        "order_id": order_id,
        "status": order_state,
        "already_processed": False,
    }, 200


@functions_framework.http
def refund_order(request: flask.Request) -> tuple[dict, int]:
    """Refunds or cancels an order once, even when the workflow retries the call."""
    order_id = (request.get_json(silent=True) or {}).get("order_id")
    if not order_id:
        return {"error": "missing order_id"}, 400
    try:
        return compensate(str(order_id))
    except Exception as err:
        if is_temporary(err):
            # Contention or a brief outage: let the workflow retry.
            return {"error": f"temporary error: {err}"}, 503
        raise  # A permanent error, such as missing permissions: fail with 500.


# [END workflows_order_saga_refund]
