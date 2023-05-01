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


def hello_world(request: flask.Request) -> flask.Response:
    """HTTP Cloud Function.

    Returns:
    - "Hello World! 👋"
    """
    response = "Hello World! 👋"

    return flask.Response(response, mimetype="text/plain")


def hello_name(request: flask.Request) -> flask.Response:
    """HTTP Cloud Function.

    Returns:
    - "Hello {NAME}! 🚀" if "name=NAME" is defined in the GET request
    - "Hello World! 🚀" otherwise
    """
    name = request.args.get("name", "World")
    response = f"Hello {name}! 🚀"

    return flask.Response(response, mimetype="text/plain")


def python_powered(request: flask.Request) -> flask.Response:
    """HTTP Cloud Function.

    Returns:
    - The official "Python Powered" logo
    """
    return flask.send_file("python-powered.png")
