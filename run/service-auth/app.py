# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from http import HTTPStatus
import os

from flask import Flask, request

from receive import receive_request_and_parse_auth_header

app = Flask(__name__)


@app.route("/")
def main() -> str:
    """Example route for receiving authorized requests."""
    try:
        response = receive_request_and_parse_auth_header(request)

        status = HTTPStatus.UNAUTHORIZED
        if "Hello" in response:
            status = HTTPStatus.OK

        return response, status
    except Exception as e:
        return f"Error verifying ID token: {e}", HTTPStatus.UNAUTHORIZED


if __name__ == "__main__":
    app.run(host="localhost", port=int(os.environ.get("PORT", 8080)), debug=True)
