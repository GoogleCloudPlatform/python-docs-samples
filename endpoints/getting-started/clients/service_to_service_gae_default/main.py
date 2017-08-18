# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0(the "License");
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

"""Example of calling a Google Cloud Endpoint API with a JWT signed by
Google App Engine Default Service Account."""

import base64
import httplib
import json
import time

from google.appengine.api import app_identity
import webapp2

DEFAULT_SERVICE_ACCOUNT = 'YOUR-CLIENT-PROJECT-ID@appspot.gserviceaccount.com'
HOST = "YOUR-SERVER-PROJECT-ID.appspot.com"


def generate_jwt():
    """Generates a signed JSON Web Token using the Google App Engine default
    service account."""
    now = int(time.time())

    header_json = json.dumps({
        "typ": "JWT",
        "alg": "RS256"})

    payload_json = json.dumps({
        'iat': now,
        # expires after one hour.
        "exp": now + 3600,
        # iss is the Google App Engine default service account email.
        'iss': DEFAULT_SERVICE_ACCOUNT,
        'sub': DEFAULT_SERVICE_ACCOUNT,
        # aud must match 'audience' in the security configuration in your
        # OpenAPI spec.It can be any string.
        'aud': 'echo.endpoints.sample.google.com',
        "email": DEFAULT_SERVICE_ACCOUNT
    })

    header_and_payload = '{}.{}'.format(
        base64.urlsafe_b64encode(header_json),
        base64.urlsafe_b64encode(payload_json))
    (key_name, signature) = app_identity.sign_blob(header_and_payload)
    signed_jwt = '{}.{}'.format(
        header_and_payload,
        base64.urlsafe_b64encode(signature))

    return signed_jwt


def make_request(signed_jwt):
    """Makes a request to the auth info endpoint for Google JWTs."""
    headers = {'Authorization': 'Bearer {}'.format(signed_jwt)}
    conn = httplib.HTTPSConnection(HOST)
    conn.request("GET", '/auth/info/googlejwt', None, headers)
    res = conn.getresponse()
    conn.close()
    return res.read()


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        signed_jwt = generate_jwt()
        res = make_request(signed_jwt)
        self.response.write(res)


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
