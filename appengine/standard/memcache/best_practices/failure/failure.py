#!/usr/bin/env python

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

import logging

from google.appengine.api import memcache
import webapp2


def read_from_persistent_store():
    """Fake method for demonstration purposes. Usually would return
     a value from a database like Cloud Datastore or MySQL."""
    return "a persistent value"


class ReadPage(webapp2.RequestHandler):
    def get(self):
        key = "some-key"
        # [START memcache-read]
        v = memcache.get(key)
        if v is None:
            v = read_from_persistent_store()
            memcache.add(key, v)
        # [END memcache-read]

        self.response.content_type = 'text/html'
        self.response.write(str(v))


class DeletePage(webapp2.RequestHandler):
    def get(self):
        key = "some key"
        seconds = 5
        memcache.set(key, "some value")
        # [START memcache-delete]
        memcache.delete(key, seconds)  # clears cache
        # write to persistent datastore
        # Do not attempt to put new value in cache, first reader will do that
        # [END memcache-delete]
        self.response.content_type = 'text/html'
        self.response.write('done')


class MainPage(webapp2.RequestHandler):
    def get(self):
        value = 3
        # [START memcache-failure]
        if not memcache.set('counter', value):
            logging.error("Memcache set failed")
            # Other error handling here
        # [END memcache-failure]
        self.response.content_type = 'text/html'
        self.response.write('done')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/delete', DeletePage),
    ('/read', ReadPage),
], debug=True)
