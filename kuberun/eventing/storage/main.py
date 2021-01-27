# Copyright 2021 Google LLC.
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

import os
import uuid

from cloudevents.http import CloudEvent, from_http, to_structured
from flask import Flask, make_response, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    # Gets the Cloud Storage bucket name from the CloudEvent header
    # Example: "storage.googleapis.com/projects/_/buckets/my-bucket"
    event = from_http(request.headers, request.get_data())
    print(
        f"Detected change in Cloud Storage bucket: {event['source']}, object: {event['subject']}"
    )

    attributes = {
        "id": str(uuid.uuid4()),
        "source": "https://localhost",
        "specversion": "1.0",
        "type": "com.example.kuberun.events.received",
    }
    data = {"message": "Event received"}
    event = CloudEvent(attributes, data)
    headers, body = to_structured(event)

    response = make_response(body, 200)
    response.headers.update(headers)
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
