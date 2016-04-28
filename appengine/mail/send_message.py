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


def send_approved_mail(sender_address):
    # [START send_message]
    message = mail.EmailMessage(
        sender=sender_address,
        subject="Your account has been approved")

    message.to = "Albert Johnson <Albert.Johnson@example.com>"
    message.body = """Dear Albert:

Your example.com account has been approved.  You can now visit
http://www.example.com/ and sign in using your Google Account to
access new features.

Please let us know if you have any questions.

The example.com Team
"""
    message.send()
    # [END send_message]


class SendMessageHandler(webapp2.RequestHandler):
    def get(self):
        send_approved_mail('{}@appspot.gserviceaccount.com'.format(
            app_identity.get_application_id()))
        self.response.content_type = 'text/plain'
        self.response.write('Sent an email message to Albert.')


app = webapp2.WSGIApplication([
    ('/send_message', SendMessageHandler),
], debug=True)
