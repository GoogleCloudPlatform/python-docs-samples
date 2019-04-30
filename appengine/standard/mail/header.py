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


def send_example_mail(sender_address, email_thread_id):
    # [START send_mail]
    mail.send_mail(sender=sender_address,
                   to="Albert Johnson <Albert.Johnson@example.com>",
                   subject="An example email",
                   body="""
The email references a given email thread id.

The example.com Team
""",
                   headers={"References": email_thread_id})
    # [END send_mail]


class SendMailHandler(webapp2.RequestHandler):
    def get(self):
        self.response.content_type = 'text/html'
        self.response.write("""<html><body><form method="POST">
          Enter an email thread id: <input name="thread_id">
          <input type=submit>
        </form></body></html>""")

    def post(self):
        print repr(self.request.POST)
        id = self.request.POST['thread_id']
        send_example_mail('{}@appspot.gserviceaccount.com'.format(
            app_identity.get_application_id()), id)
        self.response.content_type = 'text/plain'
        self.response.write(
            'Sent an email to Albert with Reference header set to {}.'
            .format(id))


app = webapp2.WSGIApplication([
    ('/header', SendMailHandler),
], debug=True)
