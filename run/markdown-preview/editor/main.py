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

import os

from flask import Flask, render_template, request

import render


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    # Render the default template
    f = open("templates/markdown.md")
    return render_template("index.html", default=f.read())


# [START cloudrun_secure_request_do]
# [START run_secure_request_do]
@app.route("/render", methods=["POST"])
def render_handler():
    body = request.get_json()
    if not body:
        return "Error rendering markdown: Invalid JSON", 400

    data = body["data"]
    try:
        parsed_markdown = render.new_request(data)
        return parsed_markdown, 200
    except Exception as err:
        return f"Error rendering markdown: {err}", 500

# [END run_secure_request_do]
# [END cloudrun_secure_request_do]


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)
