# Copyright 2020 Google, LLC.
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

# [START eventarc_http_quickstart_server]
# [START eventarc_audit_storage_server]
import os

from cloudevents.http import from_http

from flask import Flask, request

app = Flask(__name__)
# [END eventarc_audit_storage_server]
# [END eventarc_http_quickstart_server]


# [START eventarc_http_quickstart_handler]
# [START eventarc_audit_storage_handler]
@app.route("/", methods=["POST"])
def index():
    # Create a CloudEvent object from the incoming request
    event = from_http(request.headers, request.data)
    # Gets the GCS bucket name from the CloudEvent
    # Example: "storage.googleapis.com/projects/_/buckets/my-bucket"
    bucket = event.get("subject")

    print(f"Detected change in Cloud Storage bucket: {bucket}")
    return (f"Detected change in Cloud Storage bucket: {bucket}", 200)


# [END eventarc_audit_storage_handler]
# [END eventarc_http_quickstart_handler]


# [START eventarc_http_quickstart_server]
# [START eventarc_audit_storage_server]
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END eventarc_audit_storage_server]
# [END eventarc_http_quickstart_server]
