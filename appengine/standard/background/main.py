# Copyright 2016 Google Inc. All rights reserved.
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
Sample application that demonstrates how to use the App Engine background
threads.

app.yaml scaling must be set to manual or basic.
"""

# [START background-imp]
from google.appengine.api import background_thread
# [END background-imp]

import webapp2

val = 'Dog'


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(str(val))


class SetDogHandler(webapp2.RequestHandler):
    """ Resets the global val to 'Dog'"""

    def get(self):
        global val
        val = 'Dog'
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Done')


class SetCatBackgroundHandler(webapp2.RequestHandler):
    """ Demonstrates two ways to start new background threads
    """

    def get(self):
        """
        Demonstrates using a background thread to change the global
        val from 'Dog' to 'Cat'

        The auto GET parameter determines whether to start the thread
        automatically or manually
        """
        auto = self.request.get('auto')

        # [START background-start]
        # sample function to run in a background thread
        def change_val(arg):
            global val
            val = arg

        if auto:
            # Start the new thread in one command
            background_thread.start_new_background_thread(change_val, ['Cat'])
        else:
            # create a new thread and start it
            t = background_thread.BackgroundThread(
                target=change_val, args=['Cat'])
            t.start()
        # [END background-start]

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Done')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/dog', SetDogHandler),
    ('/cat', SetCatBackgroundHandler),
], debug=True)
# [END all]
