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

"""Example of calling a Google Cloud Endpoint API with a JWT signed by a
Service Account."""

import base64
import httplib
import json
import time

import googleapiclient.discovery
import httplib2
from oauth2client.contrib.appengine import AppAssertionCredentials
import webapp2

SERVICE_ACCOUNT_EMAIL = "YOUR-SERVICE-ACCOUNT-EMAIL"
HOST = "YOUR-SERVER-PROJECT-ID.appspot.com"
SERVICE_ACCOUNT = \
  "projects/YOUR-CLIENT-PROJECT-ID/serviceAccounts/YOUR-SERVICE-ACCOUNT-EMAIL"


def generate_jwt():
    """Generates a signed JSON Web Token using a service account."""
    credentials = AppAssertionCredentials(
        'https://www.googleapis.com/auth/iam')
    http_auth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build(
        serviceName='iam', version='v1', http=http_auth)

    now = int(time.time())

    header_json = json.dumps({
        "typ": "JWT",
        "alg": "RS256"})

    payload_json = json.dumps({
        'iat': now,
        # expires after one hour.
        "exp": now + 3600,
        # iss is the service account email.
        'iss': SERVICE_ACCOUNT_EMAIL,
        'sub': SERVICE_ACCOUNT_EMAIL,
        # aud must match 'audience' in the security configuration in your
        # swagger spec.It can be any string.
        'aud': 'echo.endpoints.sample.google.com',
        "email": SERVICE_ACCOUNT_EMAIL
    })

    headerAndPayload = '{}.{}'.format(
        base64.urlsafe_b64encode(header_json),
        base64.urlsafe_b64encode(payload_json))
    slist = service.projects().serviceAccounts().signBlob(
        name=SERVICE_ACCOUNT,
        body={'bytesToSign': base64.b64encode(headerAndPayload)})
    res = slist.execute()
    signature = base64.urlsafe_b64encode(
        base64.decodestring(res['signature']))
    signed_jwt = '{}.{}'.format(headerAndPayload, signature)

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
