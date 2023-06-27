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

# [START eventarc_storage_cloudevent_server]
import os

from cloudevents.http import from_http

from flask import Flask, request

from google.events.cloud.storage import StorageObjectData


app = Flask(__name__)
# [END eventarc_storage_cloudevent_server]


# [START eventarc_storage_cloudevent_handler]
@app.route("/", methods=["POST"])
def index():
    event = from_http(request.headers, request.get_data())

    # Gets the GCS bucket name from the CloudEvent data
    # Example: "storage.googleapis.com/projects/_/buckets/my-bucket"
    try:
        storage_obj = StorageObjectData(event.data)
        gcs_object = os.path.join(storage_obj.bucket, storage_obj.name)
        update_time = storage_obj.updated
        return (
            f"Cloud Storage object changed: {gcs_object}"
            + f" updated at {update_time}",
            200,
        )
    except ValueError as e:
        return (f"Failed to parse event data: {e}", 400)


# [END eventarc_storage_cloudevent_handler]


# [START eventarc_storage_cloudevent_server]
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END eventarc_storage_cloudevent_server]
