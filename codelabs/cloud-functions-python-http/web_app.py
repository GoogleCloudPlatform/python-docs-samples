# Copyright 2023 Google LLC
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

import flask

import main

app = flask.Flask(__name__)


@app.get("/")
def index():
    return main.python_powered(flask.request)


if __name__ == "__main__":
    # Local development only
    # Run "python web_app.py" and open http://localhost:8080
    app.run(host="localhost", port=8080, debug=True)
