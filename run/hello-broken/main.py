# Copyright 2019 Google, LLC.
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

# [START cloudrun_broken_service]
# [START run_broken_service]
import json
import os

from flask import Flask


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    print("hello: received request.")

    # [START cloudrun_broken_service_problem]
    # [START run_broken_service_problem]
    NAME = os.getenv("NAME")

    if not NAME:
        print("Environment validation failed.")
        raise Exception("Missing required service parameter.")
    # [END run_broken_service_problem]
    # [END cloudrun_broken_service_problem]

    return f"Hello {NAME}"


# [END run_broken_service]
# [END cloudrun_broken_service]


@app.route("/improved", methods=["GET"])
def improved():
    print("hello: received request.")

    # [START cloudrun_broken_service_upgrade]
    # [START run_broken_service_upgrade]
    NAME = os.getenv("NAME")

    if not NAME:
        NAME = "World"
        error_message = {
            "severity": "WARNING",
            "message": f"NAME not set, default to {NAME}",
        }
        print(json.dumps(error_message))
    # [END run_broken_service_upgrade]
    # [END cloudrun_broken_service_upgrade]

    return f"Hello {NAME}"


# [START cloudrun_broken_service]
# [START run_broken_service]
if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)
# [END run_broken_service]
# [END cloudrun_broken_service]
