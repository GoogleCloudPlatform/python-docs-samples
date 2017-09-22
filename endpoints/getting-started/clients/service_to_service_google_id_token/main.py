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

"""Example of calling a Google Cloud Endpoint API from Google App Engine
Default Service Account using Google ID token."""

import base64
import httplib
import json
import time
import urllib

from google.appengine.api import app_identity
import webapp2

SERVICE_ACCOUNT_EMAIL = "YOUR-CLIENT-PROJECT-ID@appspot.gserviceaccount.com"
HOST = "YOUR-SERVER-PROJECT-ID.appspot.com"
TARGET_AUD = "https://YOUR-SERVER-PROJECT-ID.appspot.com"


def generate_jwt():
    """Generates a signed JSON Web Token using the Google App Engine default
    service account."""
    now = int(time.time())

    header_json = json.dumps({
        "typ": "JWT",
        "alg": "RS256"})

    payload_json = json.dumps({
        "iat": now,
        # expires after one hour.
        "exp": now + 3600,
        # iss is the service account email.
        "iss": SERVICE_ACCOUNT_EMAIL,
        # target_audience is the URL of the target service.
        "target_audience": TARGET_AUD,
        # aud must be Google token endpoints URL.
        "aud": "https://www.googleapis.com/oauth2/v4/token"
    })

    header_and_payload = '{}.{}'.format(
        base64.urlsafe_b64encode(header_json),
        base64.urlsafe_b64encode(payload_json))
    (key_name, signature) = app_identity.sign_blob(header_and_payload)
    signed_jwt = '{}.{}'.format(
        header_and_payload,
        base64.urlsafe_b64encode(signature))

    return signed_jwt


def get_id_token():
    """Request a Google ID token using a JWT."""
    params = urllib.urlencode({
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': generate_jwt()})
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    conn = httplib.HTTPSConnection("www.googleapis.com")
    conn.request("POST", "/oauth2/v4/token", params, headers)
    res = json.loads(conn.getresponse().read())
    conn.close()
    return res['id_token']


def make_request(token):
    """Makes a request to the auth info endpoint for Google ID token."""
    headers = {'Authorization': 'Bearer {}'.format(token)}
    conn = httplib.HTTPSConnection(HOST)
    conn.request("GET", '/auth/info/googleidtoken', None, headers)
    res = conn.getresponse()
    conn.close()
    return res.read()


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        token = get_id_token()
        res = make_request(token)
        self.response.write(res)


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
