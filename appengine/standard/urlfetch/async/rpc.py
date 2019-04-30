# Copyright 2016 Google Inc. All Rights Reserved.
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

import functools
import logging

# [START urlfetch-import]
from google.appengine.api import urlfetch
# [END urlfetch-import]
import webapp2


class UrlFetchRpcHandler(webapp2.RequestHandler):
    """ Demonstrates an asynchronous HTTP query using urlfetch"""

    def get(self):
        # [START urlfetch-rpc]
        rpc = urlfetch.create_rpc()
        urlfetch.make_fetch_call(rpc, 'http://www.google.com/')

        # ... do other things ...
        try:
            result = rpc.get_result()
            if result.status_code == 200:
                text = result.content
                self.response.write(text)
            else:
                self.response.status_int = result.status_code
                self.response.write('URL returned status code {}'.format(
                    result.status_code))
        except urlfetch.DownloadError:
            self.response.status_int = 500
            self.response.write('Error fetching URL')
        # [END urlfetch-rpc]


class UrlFetchRpcCallbackHandler(webapp2.RequestHandler):
    """ Demonstrates an asynchronous HTTP query with a callback using
    urlfetch"""

    def get(self):
        # [START urlfetch-rpc-callback]
        def handle_result(rpc):
            result = rpc.get_result()
            self.response.write(result.content)
            logging.info('Handling RPC in callback: result {}'.format(result))

        urls = ['http://www.google.com',
                'http://www.github.com',
                'http://www.travis-ci.org']
        rpcs = []
        for url in urls:
            rpc = urlfetch.create_rpc()
            rpc.callback = functools.partial(handle_result, rpc)
            urlfetch.make_fetch_call(rpc, url)
            rpcs.append(rpc)

        # ... do other things ...

        # Finish all RPCs, and let callbacks process the results.

        for rpc in rpcs:
            rpc.wait()

        logging.info('Done waiting for RPCs')
        # [END urlfetch-rpc-callback]


app = webapp2.WSGIApplication([
    ('/', UrlFetchRpcHandler),
    ('/callback', UrlFetchRpcCallbackHandler),
], debug=True)
