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
Sample application that demonstrates how to use the App Engine Images API.

For more information, see README.md.
"""

# [START all]
# [START thumbnailer]
from google.appengine.api import images
from google.appengine.ext import blobstore

import webapp2


class Thumbnailer(webapp2.RequestHandler):
    def get(self):
        blob_key = self.request.get("blob_key")
        if blob_key:
            blob_info = blobstore.get(blob_key)

            if blob_info:
                img = images.Image(blob_key=blob_key)
                img.resize(width=80, height=100)
                img.im_feeling_lucky()
                thumbnail = img.execute_transforms(output_encoding=images.JPEG)

                self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(thumbnail)
                return

        # Either "blob_key" wasn't provided, or there was no value with that ID
        # in the Blobstore.
        self.error(404)
# [END thumbnailer]


app = webapp2.WSGIApplication([('/img', Thumbnailer)], debug=True)
# [END all]
