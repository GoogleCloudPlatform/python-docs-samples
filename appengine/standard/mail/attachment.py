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

from google.appengine.api import app_identity
from google.appengine.api import mail
import webapp2


# [START send_attachment]
class AttachmentHandler(webapp2.RequestHandler):
    def post(self):
        f = self.request.POST['file']
        mail.send_mail(sender='{}@appspot.gserviceaccount.com'.format(
            app_identity.get_application_id()),
                       to="Albert Johnson <Albert.Johnson@example.com>",
                       subject="The doc you requested",
                       body="""
Attached is the document file you requested.

The example.com Team
""",
                       attachments=[(f.filename, f.file.read())])
# [END send_attachment]
        self.response.content_type = 'text/plain'
        self.response.write('Sent {} to Albert.'.format(f.filename))

    def get(self):
        self.response.content_type = 'text/html'
        self.response.write("""<html><body>
            <form method="post" enctype="multipart/form-data">
              Send a file to Albert:<br />
              <input type="file" name="file"><br /><br />
              <input type="submit" name="submit" value="Submit">
            </form></body></html""")


app = webapp2.WSGIApplication([
    ('/attachment', AttachmentHandler),
], debug=True)
