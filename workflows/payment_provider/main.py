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

# A stand-in for a real payment provider, used by the idempotent_payment and
# order_saga samples. Deploy it as a Cloud Run function and set its URL as
# PAYMENT_PROVIDER_URL on the functions that call it. To simulate an ambiguous
# failure, create a document in payment_provider_faults with the charge's
# Idempotency-Key as its ID and a mode of "fail_after_charge" (charge, then
# respond 504) or "slow_after_charge" (charge, then respond after `seconds`).

# [START workflows_payment_provider]
import os
import time
import uuid

import flask
import functions_framework
from google.cloud import firestore

db = firestore.Client(database=os.environ.get("FIRESTORE_DATABASE", "(default)"))
charges = db.collection("payment_provider_charges")


@firestore.transactional
def record_charge(
    transaction: firestore.Transaction,
    charge_ref: firestore.DocumentReference,
    order_id: str,
    amount_cents: int,
) -> dict:
    """Charges once per key. Returns the charge, new or existing."""
    snapshot = charge_ref.get(transaction=transaction)
    if snapshot.exists:
        transaction.update(charge_ref, {"requests": firestore.Increment(1)})
        return snapshot.to_dict()
    charge = {
        "charge_id": uuid.uuid4().hex,
        "order_id": order_id,
        "amount_cents": amount_cents,
        "status": "charged",
        "requests": 1,
    }
    transaction.set(charge_ref, charge)
    return charge


@firestore.transactional
def record_refund(
    transaction: firestore.Transaction, charge_ref: firestore.DocumentReference
) -> bool:
    """Refunds the charge once. Returns True if money was charged and refunded.

    If the charge doesn't exist yet, voids its key, so a charge request that
    arrives late is rejected instead of charging after the refund.
    """
    snapshot = charge_ref.get(transaction=transaction)
    if not snapshot.exists:
        transaction.set(
            charge_ref, {"status": "voided", "requests": 0, "refund_requests": 1}
        )
        return False
    status = snapshot.to_dict()["status"]
    updates: dict = {"refund_requests": firestore.Increment(1)}
    if status == "charged":
        updates["status"] = "refunded"
    transaction.update(charge_ref, updates)
    return status in ("charged", "refunded")


def simulate_fault(key: str) -> tuple[dict, int] | None:
    """Applies a simulated fault for the key, if one is set."""
    fault_ref = db.collection("payment_provider_faults").document(key)
    fault = fault_ref.get()
    if not fault.exists:
        return None
    data = fault.to_dict()
    remaining = data.get("remaining", 1) - 1
    if remaining <= 0:
        fault_ref.delete()
    else:
        fault_ref.update({"remaining": remaining})
    if data.get("mode") == "fail_after_charge":
        return {"error": "gateway timeout"}, 504
    time.sleep(data.get("seconds", 40))
    return None


@functions_framework.http
def payment_provider(request: flask.Request) -> tuple[dict, int]:
    """Handles POST /charges and POST /refunds."""
    body = request.get_json(silent=True) or {}
    if request.path.endswith("/refunds"):
        # Refunds are keyed by the charge, so repeating a refund has no effect.
        charge_key = body.get("charge_key")
        if not charge_key:
            return {"error": "missing charge_key"}, 400
        refunded = record_refund(db.transaction(), charges.document(charge_key))
        fault = simulate_fault(f"refund-{charge_key}")
        if fault:
            return fault
        return {"charge_key": charge_key, "refunded": refunded}, 200

    key = request.headers.get("Idempotency-Key")
    if not key:
        return {"error": "missing Idempotency-Key"}, 400
    charge = record_charge(
        db.transaction(),
        charges.document(key),
        body.get("order_id"),
        body.get("amount_cents"),
    )
    if charge["status"] == "voided":
        return {"error": "the charge was cancelled"}, 409
    fault = simulate_fault(key)
    if fault:
        return fault
    return {"charge_id": charge["charge_id"], "status": charge["status"]}, 200


# [END workflows_payment_provider]
