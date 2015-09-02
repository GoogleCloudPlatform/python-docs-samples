# Copyright 2015 Google Inc. All rights reserved.
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
# [START all]
"""Sample appengine app demonstrating 3-legged oauth."""
import json
import os

from googleapiclient.discovery import build

from oauth2client.appengine import OAuth2DecoratorFromClientSecrets

import webapp2


# The project id whose datasets you'd like to list
PROJECTID = '<myproject_id>'

# Create the method decorator for oauth.
decorator = OAuth2DecoratorFromClientSecrets(
    os.path.join(os.path.dirname(__file__), 'client_secrets.json'),
    scope='https://www.googleapis.com/auth/bigquery')

# Create the bigquery api client
service = build('bigquery', 'v2')


class MainPage(webapp2.RequestHandler):

    @decorator.oauth_required
    def get(self):
        """Lists the datasets in PROJECTID"""
        http = decorator.http()
        datasets = service.datasets()

        response = datasets.list(projectId=PROJECTID).execute(http)

        self.response.out.write('<h3>Datasets.list raw response:</h3>')
        self.response.out.write('<pre>%s</pre>' %
                                json.dumps(response, sort_keys=True, indent=4,
                                           separators=(',', ': ')))


# Create the webapp2 application
app = webapp2.WSGIApplication([
    ('/', MainPage),
    # Create the endpoint to receive oauth flow callbacks
    (decorator.callback_path, decorator.callback_handler())
], debug=True)
# [END all]
