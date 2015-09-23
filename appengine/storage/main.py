#!/usr/bin/env python

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

"""Present formatted listings for Google Cloud Storage buckets.
This Google App Engine application takes a bucket name in the URL path and uses
the Google Cloud Storage JSON API and Google's Python client library to list
the bucket's contents.
For example, if this app is invoked with the URI
http://bucket-list.appspot.com/foo, it would extract the bucket name 'foo' and
issue a request to GCS for its contents. The app formats the listing into an
XML document, which is prepended with a reference to an XSLT style sheet for
human readable presentation.
For more information:
Google APIs Client Library for Python:
  <https://code.google.com/p/google-api-python-client/>
Google Cloud Storage JSON API:
  <https://developers.google.com/storage/docs/json_api/>
Using OAuth 2.0 for Server to Server Applications:
  <https://developers.google.com/accounts/docs/OAuth2ServiceAccount>
App Identity Python API Overview:
  <https://code.google.com/appengine/docs/python/appidentity/overview.html>
"""

import os

from apiclient.discovery import build as build_service
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required
import httplib2
import jinja2
from oauth2client.client import OAuth2WebServerFlow

# NOTE: You must provide a client ID and secret with access to the GCS JSON
# API.
# You can acquire a client ID and secret from the Google Developers Console.
#   <https://developers.google.com/console#:access>
CLIENT_ID = ''
CLIENT_SECRET = ''
SCOPE = 'https://www.googleapis.com/auth/devstorage.read_only'
USER_AGENT = 'app-engine-bucket-lister'

# Since we don't plan to use all object attributes, we pass a fields argument
# to specify what the server should return.
FIELDS = 'items(name,media(timeCreated,hash,length))'


def GetBucketName(path):
    bucket = path[1:]  # Trim the preceding slash
    if bucket[-1] == '/':
        # Trim final slash, if necessary.
        bucket = bucket[:-1]
    return bucket


class MainHandler(webapp.RequestHandler):
    @login_required
    def get(self):
        callback = self.request.host_url + '/oauth2callback'
        flow = OAuth2WebServerFlow(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=callback,
            access_type='online',
            scope=SCOPE,
            user_agent=USER_AGENT)

        bucket = GetBucketName(self.request.path)
        step2_url = flow.step1_get_authorize_url()
        # Add state to remember which bucket to list.
        self.redirect(step2_url + '&state=%s' % bucket)


class AuthHandler(webapp.RequestHandler):
    @login_required
    def get(self):
        callback = self.request.host_url + '/oauth2callback'
        flow = OAuth2WebServerFlow(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=callback,
            scope=SCOPE,
            user_agent=USER_AGENT)

        # Exchange the code (in self.request.params) for an access token.
        credentials = flow.step2_exchange(self.request.params)
        http = credentials.authorize(httplib2.Http())

        bucket = self.request.get('state')
        storage = build_service('storage', 'v1beta1', http=http)
        list_response = storage.objects().list(bucket=bucket,
                                               fields=FIELDS).execute()
        template_values = {
            'items': list_response['items'], 'bucket_name': bucket}

        # We use a templating engine to format our output. For more
        # information:
        #   <http://jinja.pocoo.org/docs/>
        jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
        template = jinja_env.get_template('listing.html')
        self.response.out.write(template.render(template_values))


app = webapp.WSGIApplication(
    [
        ('/oauth2callback', AuthHandler),
        ('/..*', MainHandler)
    ],
    debug=True)
