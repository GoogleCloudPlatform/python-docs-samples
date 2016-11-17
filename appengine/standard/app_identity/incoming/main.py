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
Sample Google App Engine application that demonstrates usage of the app
engine inbound app ID header.

For more information about App Engine, see README.md under /appengine.
"""

# [START all]
import webapp2


class MainPage(webapp2.RequestHandler):
    allowed_app_ids = [
        'other-app-id',
        'other-app-id-2'
    ]

    def get(self):
        incoming_app_id = self.request.headers.get(
            'X-Appengine-Inbound-Appid', None)

        if incoming_app_id not in self.allowed_app_ids:
            self.abort(403)

        self.response.write('This is a protected page.')


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)

# [END all]
