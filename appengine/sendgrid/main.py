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

import sendgrid
import webapp2

# make a secure connection to SendGrid
SENDGRID_API_KEY = 'your-sendgrid-api-key'
SENDGRID_DOMAIN = 'your-sendgrid-domain'

sg = sendgrid.SendGridClient(SENDGRID_API_KEY)


def send_simple_message(recipient):
    message = sendgrid.Mail()
    message.set_subject('message subject')
    message.set_html('<strong>HTML message body</strong>')
    message.set_text('plaintext message body')
    message.set_from('from: Example Sender <mailgun@{}>'.format(
     SENDGRID_DOMAIN))
    message.set_from('App Engine App <sendgrid@{}>'.format(SENDGRID_DOMAIN))
    message.add_to(recipient)
    status, msg = sg.send(message)
    return (status, msg)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.content_type = 'text/html'
        self.response.write("""
<!doctype html>
<html><body>
<form action="/send" method="POST">
<input type="text" name="recipient" placeholder="Enter recipient email">
<input type="submit" name="submit" value="Send simple email">
</form>
</body></html>
""")


class SendEmailHandler(webapp2.RequestHandler):
    def post(self):
        recipient = self.request.get('recipient')
        (status, msg) = send_simple_message(recipient)
        self.response.set_status(status)
        if status == 200:
            self.response.write(msg)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/send', SendEmailHandler)
], debug=True)
