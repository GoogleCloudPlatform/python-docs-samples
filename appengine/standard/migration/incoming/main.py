# Copyright 2020 Google LLC
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

"""
Authenticate requests coming from other App Engine instances.
"""

# [START gae_python_app_identity_incoming]
from google.oauth2 import id_token
from google.auth.transport import requests

import logging
import webapp2


def get_app_id(request):
    # Requests from App Engine Standard for Python 2.7 will include a
    # trustworthy X-Appengine-Inbound-Appid. Other requests won't have
    # that header, as the App Engine runtime will strip it out
    incoming_app_id = request.headers.get(
        'X-Appengine-Inbound-Appid', None)
    if incoming_app_id is not None:
        return incoming_app_id

    # Other App Engine apps can get an ID token for the App Engine default
    # service account, which will identify the application ID. They will
    # have to include at token in an Authorization header to be recognized
    # by this method.
    auth_header = request.headers.get('Authorization', None)
    if auth_header is None:
        return None

    # The auth_header must be in the form Authorization: Bearer token.
    bearer, token = auth_header.split()
    if bearer.lower() != 'bearer':
        return None

    try:
        info = id_token.verify_oauth2_token(token, requests.Request())
        service_account_email = info['email']
        incoming_app_id, domain = service_account_email.split('@')
        if domain != 'appspot.gserviceaccount.com':  # Not App Engine svc acct
            return None
        else:
            return incoming_app_id
    except Exception as e:
        # report or log if desired, as here:
        logging.warning('Request has bad OAuth2 id token: {}'.format(e))
        return None


class MainPage(webapp2.RequestHandler):
    allowed_app_ids = [
        'other-app-id',
        'other-app-id-2'
    ]

    def get(self):
        incoming_app_id = get_app_id(self.request)

        if incoming_app_id is None:
            self.abort(403)

        if incoming_app_id not in self.allowed_app_ids:
            self.abort(403)

        self.response.write('This is a protected page.')


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
# [END gae_python_app_identity_incoming]
