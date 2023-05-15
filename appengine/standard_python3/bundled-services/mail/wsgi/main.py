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

import cgi
import http
import os
import re

from google.appengine.api import mail
from google.appengine.api import wrap_wsgi_app


# [START gae_mail_handler_receive_wsgi]
def HelloReceiver(environ, start_response):
    if environ["REQUEST_METHOD"] != "POST":
        return ("", http.HTTPStatus.METHOD_NOT_ALLOWED, [("Allow", "POST")])

    message = mail.InboundEmailMessage.from_environ(environ)

    print(f"Received greeting for {message.to} at {message.date} from {message.sender}")
    for content_type, payload in message.bodies("text/plain"):
        print(f"Text/plain body: {payload.decode()}")
        break

    response = http.HTTPStatus.OK
    start_response(f"{response.value} {response.phrase}", [])
    return ["success".encode("utf-8")]


# [END gae_mail_handler_receive_wsgi]


# [START gae_mail_handler_bounce_wsgi]
def BounceReceiver(environ, start_response):
    if environ["REQUEST_METHOD"] != "POST":
        return ("", http.HTTPStatus.METHOD_NOT_ALLOWED, [("Allow", "POST")])

    bounce_message = mail.BounceNotification.from_environ(environ)

    # Do something with the message
    print("Bounce original: ", bounce_message.original)
    print("Bounce notification: ", bounce_message.notification)

    # Return suitable response
    response = http.HTTPStatus.OK
    start_response(f"{response.value} {response.phrase}", [])
    return ["success".encode("utf-8")]


# [END gae_mail_handler_bounce_wsgi]


def HomePage(environ, start_response):
    if environ["REQUEST_METHOD"] == "GET":
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
        response = http.HTTPStatus.OK
        start_response(f"{response.value} {response.phrase}", [])
        return [html.encode("utf-8")]

    else:  # POST request
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

        form = cgi.parse(environ["wsgi.input"])

        address = form.get("email")[0]
        if address is None:
            print("Error: missing email address")
            return "Error: Missing email address", 400

        try:
            mail.send_mail(
                sender=f"demo-app@{project_id}.appspotmail.com",
                to=address,
                subject="App Engine Outgoing Email",
                body=form.get("body")[0],
            )
        except Exception as e:
            print(f"Sending mail to {address} failed with exception {e}.")
            start_response("500 SERVER ERROR")
            return [f"Exception {e} when sending mail to {address}.".encode("utf-8")]

        print(f"Successfully sent mail to {address}.")

        response = http.HTTPStatus.CREATED
        start_response(f"{response.value} {response.phrase}", [])
        return [f"Successfully sent mail to {address}.".encode()]


routes = {
    mail.INCOMING_MAIL_URL_PATTERN: HelloReceiver,
    mail.BOUNCE_NOTIFICATION_URL_PATH: BounceReceiver,
    "": HomePage,
}


class WSGIApplication:
    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")
        for regex, callable in routes.items():
            match = re.search(regex, path)
            if match is not None:
                return callable(environ, start_response)
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return ["Not found".encode("utf-8")]


app = wrap_wsgi_app(WSGIApplication())
