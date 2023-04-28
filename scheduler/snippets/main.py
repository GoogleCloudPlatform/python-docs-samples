# Copyright 2019 Google LLC
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

"""App Engine app to serve as an endpoint for Cloud Scheduler samples."""

# [START cloudscheduler_app]
from flask import Flask, request

app = Flask(__name__)


# Define relative URI for job endpoint
@app.route("/log_payload", methods=["POST"])
def example_task_handler():
    """Log the job payload."""
    payload = request.get_data(as_text=True) or "(empty payload)"
    print(f"Received job with payload: {payload}")
    return f"Printed job payload: {payload}"


# [END cloudscheduler_app]


@app.route("/")
def hello():
    """Basic index to verify app is serving."""
    return "Hello World!"


if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
