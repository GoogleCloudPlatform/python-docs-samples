# Copyright 2015 Google LLC.
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

# [START app]
import logging
import subprocess

from flask import Flask


app = Flask(__name__)


# [START example]
@app.route("/")
def fortune():
    """Runs the 'fortune' command and serves the output.

    Returns:
        The output of the 'fortune' command.
    """
    output = subprocess.check_output("/usr/games/fortune")
    return output, 200, {"Content-Type": "text/plain; charset=utf-8"}


# [END example]


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
    # application on Google App Engine. See CMD in Dockerfile.
    app.run(host="127.0.0.1", port=8080, debug=True)
# [END app]
