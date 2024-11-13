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

# [START app]
import base64
import json
import logging
import os

from flask import current_app, Flask, render_template, request
from google.auth.transport import requests
from google.cloud import pubsub_v1
from google.oauth2 import id_token


app = Flask(__name__)

# Configure the following environment variables via app.yaml
# This is used in the push request handler to verify that the request came from
# pubsub and originated from a trusted source.
app.config["PUBSUB_VERIFICATION_TOKEN"] = os.environ["PUBSUB_VERIFICATION_TOKEN"]
app.config["PUBSUB_TOPIC"] = os.environ["PUBSUB_TOPIC"]
app.config["GOOGLE_CLOUD_PROJECT"] = os.environ["GOOGLE_CLOUD_PROJECT"]

# Global list to store messages, tokens, etc. received by this instance.
MESSAGES = []
TOKENS = []
CLAIMS = []


# [START index]
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template(
            "index.html", messages=MESSAGES, tokens=TOKENS, claims=CLAIMS
        )

    data = request.form.get("payload", "Example payload").encode("utf-8")

    # Consider initializing the publisher client outside this function
    # for better latency performance.
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(
        app.config["GOOGLE_CLOUD_PROJECT"], app.config["PUBSUB_TOPIC"]
    )
    future = publisher.publish(topic_path, data)
    future.result()
    return "OK", 200


# [END index]


# [START gae_standard_pubsub_auth_push]
@app.route("/push-handlers/receive_messages", methods=["POST"])
def receive_messages_handler():
    # Verify that the request originates from the application.
    if request.args.get("token", "") != current_app.config["PUBSUB_VERIFICATION_TOKEN"]:
        return "Invalid request", 400

    # Verify that the push request originates from Cloud Pub/Sub.
    try:
        # Get the Cloud Pub/Sub-generated JWT in the "Authorization" header.
        bearer_token = request.headers.get("Authorization")
        token = bearer_token.split(" ")[1]
        TOKENS.append(token)

        # Verify and decode the JWT. `verify_oauth2_token` verifies
        # the JWT signature, the `aud` claim, and the `exp` claim.
        # Note: For high volume push requests, it would save some network
        # overhead if you verify the tokens offline by downloading Google's
        # Public Cert and decode them using the `google.auth.jwt` module;
        # caching already seen tokens works best when a large volume of
        # messages have prompted a single push server to handle them, in which
        # case they would all share the same token for a limited time window.
        claim = id_token.verify_oauth2_token(
            token, requests.Request(), audience="example.com"
        )

        # IMPORTANT: you should validate claim details not covered by signature
        # and audience verification above, including:
        #   - Ensure that `claim["email"]` is equal to the expected service
        #     account set up in the push subscription settings.
        #   - Ensure that `claim["email_verified"]` is set to true.

        CLAIMS.append(claim)
    except Exception as e:
        return f"Invalid token: {e}\n", 400

    envelope = json.loads(request.data.decode("utf-8"))
    payload = base64.b64decode(envelope["message"]["data"])
    MESSAGES.append(payload)
    # Returning any 2xx status indicates successful receipt of the message.
    return "OK", 200


# [END gae_standard_pubsub_auth_push]

# [START gae_standard_pubsub_push]
@app.route("/pubsub/push", methods=["POST"])
def receive_pubsub_messages_handler():
    # Verify that the request originates from the application.
    if request.args.get("token", "") != current_app.config["PUBSUB_VERIFICATION_TOKEN"]:
        return "Invalid request", 400

    envelope = json.loads(request.data.decode("utf-8"))
    payload = base64.b64decode(envelope["message"]["data"])
    MESSAGES.append(payload)
    # Returning any 2xx status indicates successful receipt of the message.
    return "OK", 200

# [END gae_standard_pubsub_push]


@app.errorhandler(500)
def server_error(e):
    logging.exception("An error occurred during a request.")
    return (
        """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(
            e
        ),
        500,
    )


if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
# [END app]
