#!/usr/bin/env python

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
Sample Google App Engine application that demonstrates how to send mail using
Mailgun.

For more information, see README.md.
"""

from urllib import urlencode

import httplib2
import webapp2


# Your Mailgun Domain Name
MAILGUN_DOMAIN_NAME = 'your-mailgun-domain-name'
# Your Mailgun API key
MAILGUN_API_KEY = 'your-mailgun-api-key'


# [START simple_message]
def send_simple_message(recipient):
    http = httplib2.Http()
    http.add_credentials('api', MAILGUN_API_KEY)

    url = 'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN_NAME)
    data = {
        'from': 'Example Sender <mailgun@{}>'.format(MAILGUN_DOMAIN_NAME),
        'to': recipient,
        'subject': 'This is an example email from Mailgun',
        'text': 'Test message from Mailgun'
    }

    resp, content = http.request(
        url, 'POST', urlencode(data),
        headers={"Content-Type": "application/x-www-form-urlencoded"})

    if resp.status != 200:
        raise RuntimeError(
            'Mailgun API error: {} {}'.format(resp.status, content))
# [END simple_message]


# [START complex_message]
def send_complex_message(recipient):
    http = httplib2.Http()
    http.add_credentials('api', MAILGUN_API_KEY)

    url = 'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN_NAME)
    data = {
        'from': 'Example Sender <mailgun@{}>'.format(MAILGUN_DOMAIN_NAME),
        'to': recipient,
        'subject': 'This is an example email from Mailgun',
        'text': 'Test message from Mailgun',
        'html': '<html>HTML <strong>version</strong> of the body</html>'
    }

    resp, content = http.request(
        url, 'POST', urlencode(data),
        headers={"Content-Type": "application/x-www-form-urlencoded"})

    if resp.status != 200:
        raise RuntimeError(
            'Mailgun API error: {} {}'.format(resp.status, content))
# [END complex_message]


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.content_type = 'text/html'
        self.response.write("""
<!doctype html>
<html><body>
<form method="POST">
<input type="text" name="recipient" placeholder="Enter recipient email">
<input type="submit" name="submit" value="Send simple email">
<input type="submit" name="submit" value="Send complex email">
</form>
</body></html>
""")

    def post(self):
        recipient = self.request.get('recipient')
        action = self.request.get('submit')

        if action == 'Send simple email':
            send_simple_message(recipient)
        else:
            send_complex_message(recipient)

        self.response.write('Mail sent')


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
