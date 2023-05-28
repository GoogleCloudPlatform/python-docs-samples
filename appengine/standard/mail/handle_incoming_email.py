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

# [START gae_mail_log_sender_handler]
import logging

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
import webapp2


class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)
# [END gae_mail_log_sender_handler]
# [START gae_mail_bodies]
        plaintext_bodies = mail_message.bodies('text/plain')
        html_bodies = mail_message.bodies('text/html')

        for content_type, body in html_bodies:
            decoded_html = body.decode()
            # ...
# [END gae_mail_bodies]
            logging.info("Html body of length %d.", len(decoded_html))
        for content_type, body in plaintext_bodies:
            plaintext = body.decode()
            logging.info("Plain text body of length %d.", len(plaintext))


# [START gae_mail_app]
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
# [END gae_mail_app]
