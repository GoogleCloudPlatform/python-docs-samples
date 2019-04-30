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


from google.appengine.api import memcache
import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        # [START sharing]
        self.response.headers['Content-Type'] = 'text/plain'

        who = memcache.get('who')
        self.response.write('Previously incremented by %s\n' % who)
        memcache.set('who', 'Python')

        count = memcache.incr('count', 1, initial_value=0)
        self.response.write('Count incremented by Python = %s\n' % count)
        # [END sharing]


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
