# Copyright 2022 Google LLC
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

import os

from flask import Flask, request
from google.appengine.api import mail
from google.appengine.api import wrap_wsgi_app

app = Flask(__name__)

# Enable access to bundled services
app.wsgi_app = wrap_wsgi_app(app.wsgi_app)


@app.route("/", methods=["GET"])
def home_page():
    html = """
<!DOCTYPE html5>
<html>
<head><title>App Engine Legacy Mail</title></head>
<body>
    <h1>Send Email from App Engine</h1>

    <form action="" method="POST">
        <label for="email">Send email to address: </label>
        <input type="text" name="email" id="email" size="40"/>
        <br />
        <label for="body">With this body: </label>
        <input type="text" name="body" id="body" size="40"/>
        <br />
        <input type="submit" value="Send" />
    </form>
</body>
"""
    return html


@app.route("/", methods=["POST"])
def send_mail():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    address = request.form.get("email")
    if address is None:
        print("Error: missing email address")
        return "Error: Missing email address", 400

    try:
        mail.send_mail(
            sender=f"demo-app@{project_id}.appspotmail.com",
            to=address,
            subject="App Engine Outgoing Email",
            body=request.form.get("body"),
        )
    except Exception as e:
        print(f"Sending mail to {address} failed with exception {e}.")
        return f"Exception {e} when sending mail to {address}.", 500

    print(f"Successfully sent mail to {address}.")
    return f"Successfully sent mail to {address}.", 201


# [START gae_mail_handler_bounce_flask]
@app.route("/_ah/bounce", methods=["POST"])
def receive_bounce():
    bounce_message = mail.BounceNotification(dict(request.form.lists()))

    # Do something with the message
    print("Bounce original: ", bounce_message.original)
    print("Bounce notification: ", bounce_message.notification)

    return "OK", 200


# [END gae_mail_handler_bounce_flask]


# [START gae_mail_handler_receive_flask]
@app.route("/_ah/mail/<path>", methods=["POST"])
def receive_mail(path):
    message = mail.InboundEmailMessage(request.get_data())

    # Do something with the message
    print(f"Received greeting for {message.to} at {message.date} from {message.sender}")
    for content_type, payload in message.bodies("text/plain"):
        print(f"Text/plain body: {payload.decode()}")
        break

    return "OK", 200


# [END gae_mail_handler_receive_flask]
