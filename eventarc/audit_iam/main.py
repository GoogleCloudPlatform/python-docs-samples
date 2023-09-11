# Copyright 2023 Google LLC.
#
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

# [START eventarc_audit_iam_server]
import json
import os

from cloudevents.http import from_http
from flask import Flask, request
from google.events.cloud.audit import LogEntryData

app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# [END eventarc_audit_iam_server]


# [START eventarc_audit_iam_handler]
@app.route("/", methods=["POST"])
def index():
    # Transform the HTTP request into a CloudEvent
    event = from_http(request.headers, request.get_data())

    # Extract the LogEntryData from the CloudEvent
    # The LogEntryData type is described at https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry
    # re-serialize to json, to convert the json-style 'lowerCamelCase' names to the protobuf-style 'snake_case' equivalents.
    # ignore_unknown_fields is needed to skip the '@type' fields.
    log_entry = LogEntryData.from_json(
        json.dumps(event.get_data()), ignore_unknown_fields=True
    )

    # Ensure that this event is for service accout key creation, and succeeded.
    if log_entry.proto_payload.service_name != "iam.googleapis.com":
        return ("Received event was not from IAM.", 400)
    if log_entry.proto_payload.status.code != 0:
        return ("Key creation failed, not reporting.", 204)

    # Extract relevant fields from the audit log entry.
    # Identify the user that requested key creation
    user = log_entry.proto_payload.authentication_info.principal_email

    # Extract the resource name from the CreateServiceAccountKey request
    # For details of this type, see https://cloud.google.com/iam/docs/reference/rpc/google.iam.admin.v1#createserviceaccountkeyrequest
    service_account = log_entry.proto_payload.request["name"]

    # The response is of type google.iam.admin.v1.ServiceAccountKey,
    # which is described at https://cloud.google.com/iam/docs/reference/rpc/google.iam.admin.v1#google.iam.admin.v1.ServiceAccountKey
    # This key path can be used with gcloud to disable/delete the key:
    # e.g. gcloud iam service-accounts keys disable ${keypath}
    keypath = log_entry.proto_payload.response["name"]

    print(f"New Service Account Key created for {service_account} by {user}: {keypath}")
    return (
        f"New Service Account Key created for {service_account} by {user}: {keypath}",
        200,
    )


# [END eventarc_audit_iam_handler]
