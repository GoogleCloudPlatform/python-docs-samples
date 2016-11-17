# Copyright 2015 Google Inc.
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
Sample Google App Engine application that demonstrates using the App Engine
identity API to generate an auth token.

For more information about App Engine, see README.md under /appengine.
"""

# [START all]
import json
import logging

from google.appengine.api import app_identity
from google.appengine.api import urlfetch
import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        auth_token, _ = app_identity.get_access_token(
            'https://www.googleapis.com/auth/cloud-platform')
        logging.info(
            'Using token {} to represent identity {}'.format(
                auth_token, app_identity.get_service_account_name()))

        response = urlfetch.fetch(
            'https://www.googleapis.com/storage/v1/b?project={}'.format(
                app_identity.get_application_id()),
            method=urlfetch.GET,
            headers={
                'Authorization': 'Bearer {}'.format(auth_token)
            }
        )

        if response.status_code != 200:
            raise Exception(
                'Call failed. Status code {}. Body {}'.format(
                    response.status_code, response.content))

        result = json.loads(response.content)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(result, indent=2))


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)

# [END all]
