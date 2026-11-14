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

# A stand-in for a fulfillment service, used by the order_saga sample. Deploy
# it as a Cloud Run function and set its URL as FULFILLMENT_URL on the saga
# workflow. To simulate a failure that the saga must compensate for, create a
# document in fulfillment_service_faults with the order ID as its ID.

# [START workflows_fulfillment_service]
import os

import flask
import functions_framework
from google.cloud import firestore

db = firestore.Client(database=os.environ.get("FIRESTORE_DATABASE", "(default)"))


@functions_framework.http
def fulfill(request: flask.Request) -> tuple[dict, int]:
    """Fulfills the order, or fails permanently if it's out of stock."""
    raw_order_id = (request.get_json(silent=True) or {}).get("order_id")
    if not raw_order_id:
        return {"error": "missing order_id"}, 400
    order_id = str(raw_order_id)
    if db.collection("fulfillment_service_faults").document(order_id).get().exists:
        # 422 is permanent, so the workflow doesn't retry it and runs the refund.
        return {"error": "out of stock"}, 422
    return {"order_id": order_id, "status": "fulfilled"}, 200


# [END workflows_fulfillment_service]
