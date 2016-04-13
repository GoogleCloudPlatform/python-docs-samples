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

"""
Sample application that demonstrates various aspects of App Engine's request
handling.
"""

import os
import time

import webapp2


# [START request_timer]
class TimerHandler(webapp2.RequestHandler):
    def get(self):
        from google.appengine.runtime import DeadlineExceededError

        try:
            time.sleep(70)
            self.response.write('Completed.')
        except DeadlineExceededError:
            self.response.clear()
            self.response.set_status(500)
            self.response.out.write(
                'The request did not complete in time.')
# [END request_timer]


# [START environment]
class PrintEnvironmentHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        for key, value in os.environ.iteritems():
            self.response.out.write(
                "{} = {}\n".format(key, value))
# [END environment]


# [START request_ids]
class RequestIdHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        request_id = os.environ.get('REQUEST_LOG_ID')
        self.response.write(
            'REQUEST_LOG_ID={}'.format(request_id))
# [END request_ids]


app = webapp2.WSGIApplication([
    ('/timer', TimerHandler),
    ('/environment', PrintEnvironmentHandler),
    ('/requestid', RequestIdHandler)
], debug=True)
