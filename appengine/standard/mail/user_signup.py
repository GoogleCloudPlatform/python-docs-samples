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

import datetime
import random
import socket
import string

from google.appengine.api import app_identity
from google.appengine.api import mail
from google.appengine.ext import ndb
import webapp2


# [START send-confirm-email]
class UserSignupHandler(webapp2.RequestHandler):
    """Serves the email address sign up form."""

    def post(self):
        user_address = self.request.get('email_address')

        if not mail.is_email_valid(user_address):
            self.get()  # Show the form again.
        else:
            confirmation_url = create_new_user_confirmation(user_address)
            sender_address = (
                'Example.com Support <{}@appspot.gserviceaccount.com>'.format(
                    app_identity.get_application_id()))
            subject = 'Confirm your registration'
            body = """Thank you for creating an account!
Please confirm your email address by clicking on the link below:

{}
""".format(confirmation_url)
            mail.send_mail(sender_address, user_address, subject, body)
# [END send-confirm-email]
            self.response.content_type = 'text/plain'
            self.response.write('An email has been sent to {}.'.format(
                user_address))

    def get(self):
        self.response.content_type = 'text/html'
        self.response.write("""<html><body><form method="POST">
        Enter your email address: <input name="email_address">
        <input type=submit>
        </form></body></html>""")


class UserConfirmationRecord(ndb.Model):
    """Datastore record with email address and confirmation code."""
    user_address = ndb.StringProperty(indexed=False)
    confirmed = ndb.BooleanProperty(indexed=False, default=False)
    timestamp = ndb.DateTimeProperty(indexed=False, auto_now_add=True)


def create_new_user_confirmation(user_address):
    """Create a new user confirmation.

    Args:
        user_address: string, an email addres

    Returns: The url to click to confirm the email address."""
    id_chars = string.ascii_letters + string.digits
    rand = random.SystemRandom()
    random_id = ''.join([rand.choice(id_chars) for i in range(42)])
    record = UserConfirmationRecord(user_address=user_address,
                                    id=random_id)
    record.put()
    return 'https://{}/user/confirm?code={}'.format(
        socket.getfqdn(socket.gethostname()), random_id)


class ConfirmUserSignupHandler(webapp2.RequestHandler):
    """Invoked when the user clicks on the confirmation link in the email."""

    def get(self):
        code = self.request.get('code')
        if code:
            record = ndb.Key(UserConfirmationRecord, code).get()
            # 2-hour time limit on confirming.
            if record and (datetime.datetime.now() - record.timestamp <
                           datetime.timedelta(hours=2)):
                record.confirmed = True
                record.put()
                self.response.content_type = 'text/plain'
                self.response.write('Confirmed {}.'
                                    .format(record.user_address))
                return
        self.response.status_int = 404


app = webapp2.WSGIApplication([
    ('/user/signup', UserSignupHandler),
    ('/user/confirm', ConfirmUserSignupHandler),
], debug=True)
