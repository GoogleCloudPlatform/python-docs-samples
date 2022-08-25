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

from django.conf import settings
from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from google.appengine.api import mail
from google.appengine.api import wrap_wsgi_app


def home_page(request):
    """
    Return a form asking about mail to send in reponse to a GET request,
    and process the form and send the mail when the form is POSTed.
    """

    if request.method == "GET":
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
        return HttpResponse(html)
    else:
        return send_mail(request.POST.get("email"), request.POST.get("body"))


def send_mail(address, body):
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if address is None:
        return HttpResponse(content="Error: Missing email address", status=400)

    try:
        mail.send_mail(
            sender=f"demo-app@{project_id}.appspotmail.com",
            to=address,
            subject="App Engine Outgoing Email",
            body=body,
        )
    except Exception as e:
        print(f"Sending mail to {address} failed with exception {e}.")
        return HttpResponse(
            content=f"Exception {e} when sending mail to {address}.",
            status=500,
        )

    print(f"Successfully sent mail to {address}.")
    return HttpResponse(content=f"Successfully sent mail to {address}.", status=201)


# [START gae_mail_handler_receive_django]
def receive_mail(request):
    message = mail.InboundEmailMessage(request.body)

    print(f"Received greeting for {message.to} at {message.date} from {message.sender}")
    for _, payload in message.bodies("text/plain"):
        print(f"Text/plain body: {payload.decode()}")
        break

    return HttpResponse("OK")


# [END gae_mail_handler_receive_django]


# [START gae_mail_handler_bounce_django]
def receive_bounce(request):
    bounce_message = mail.BounceNotification(dict(request.POST.lists()))

    # Do something with the message
    print(f"Bounce original: {bounce_message.original}")
    print(f"Bounce notification: {bounce_message.notification}")

    return HttpResponse("OK")


# [END gae_mail_handler_bounce_django]


urlpatterns = [
    url(r"^$", home_page),
    url(r"^_ah/mail/.*$", receive_mail),
    url(r"^_ah/bounce$", receive_bounce),
]

settings.configure(
    DEBUG=True,
    SECRET_KEY="thisisthesecretkey",
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ),
)

app = wrap_wsgi_app(get_wsgi_application())
