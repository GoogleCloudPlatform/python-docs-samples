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

"""
Sample Google App Engine application that demonstrates using appstats.

For more information about App Engine, see README.md under /appengine.
"""

# [START all]
from google.appengine.api import memcache
import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        # Perform some RPCs so that appstats can capture them.
        memcache.set('example_key', 50)
        value = memcache.get('example_key')
        self.response.write('Value is: {}'.format(value))


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
# [END all]
