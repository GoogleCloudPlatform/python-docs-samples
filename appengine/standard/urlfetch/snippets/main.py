# Copyright 2016 Google Inc.
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

"""Sample application that demonstrates different ways of fetching
URLS on App Engine.
"""

import logging
import urllib

# [START gae_urlfetch_snippets_imports_urllib2]
import urllib2
# [END gae_urlfetch_snippets_imports_urllib2]

# [START gae_urlfetch_snippets_imports_urlfetch]
from google.appengine.api import urlfetch
# [END gae_urlfetch_snippets_imports_urlfetch]

import webapp2


class UrlLibFetchHandler(webapp2.RequestHandler):
    """Demonstrates an HTTP query using urllib2."""

    def get(self):
        # [START gae_urlfetch_snippets_urllib2_get]
        url = "http://www.google.com/humans.txt"
        try:
            result = urllib2.urlopen(url)
            self.response.write(result.read())
        except urllib2.URLError:
            logging.exception("Caught exception fetching url")
        # [END gae_urlfetch_snippets_urllib2_get]


class UrlFetchHandler(webapp2.RequestHandler):
    """Demonstrates an HTTP query using urlfetch."""

    def get(self):
        # [START gae_urlfetch_snippets_urlfetch_get]
        url = "http://www.google.com/humans.txt"
        try:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                self.response.write(result.content)
            else:
                self.response.status_code = result.status_code
        except urlfetch.Error:
            logging.exception("Caught exception fetching url")
        # [END gae_urlfetch_snippets_urlfetch_get]


class UrlPostHandler(webapp2.RequestHandler):
    """Demonstrates an HTTP POST form query using urlfetch."""

    form_fields = {
        "first_name": "Albert",
        "last_name": "Johnson",
    }

    def get(self):
        # [START gae_urlfetch_snippets_urlfetch_post]
        try:
            form_data = urllib.urlencode(UrlPostHandler.form_fields)
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            result = urlfetch.fetch(
                url="http://localhost:8080/submit_form",
                payload=form_data,
                method=urlfetch.POST,
                headers=headers,
            )
            self.response.write(result.content)
        except urlfetch.Error:
            logging.exception("Caught exception fetching url")
        # [END gae_urlfetch_snippets_urlfetch_post]


class SubmitHandler(webapp2.RequestHandler):
    """Handler that receives UrlPostHandler POST request."""

    def post(self):
        self.response.out.write((self.request.get("first_name")))


app = webapp2.WSGIApplication(
    [
        ("/", UrlLibFetchHandler),
        ("/url_fetch", UrlFetchHandler),
        ("/url_post", UrlPostHandler),
        ("/submit_form", SubmitHandler),
    ],
    debug=True,
)
