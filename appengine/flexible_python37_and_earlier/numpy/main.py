# Copyright 2016 Google LLC.
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

import logging

from flask import Flask
import numpy as np

app = Flask(__name__)


@app.route("/")
def calculate():
    """Performs a dot product on predefined arrays.

    Returns:
        Returns a formatted message containing the dot product result of
        two predefined arrays.
    """
    return_str = ""
    x = np.array([[1, 2], [3, 4]])
    y = np.array([[5, 6], [7, 8]])

    return_str += f"x: {str(x)} , y: {str(y)}<br />"

    # Multiply matrices
    return_str += f"x dot y : {str(np.dot(x, y))}"
    return return_str


@app.errorhandler(500)
def server_error(e):
    """Serves a formatted message on-error.

    Returns:
        The error message and a code 500 status.
    """
    logging.exception("An error occurred during a request.")
    return (
        f"An internal error occurred: <pre>{e}</pre><br>See logs for full stacktrace.",
        500,
    )


if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
