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

import logging

from google.appengine.api import xmpp

import mock
import webapp2

# Mock roster of users
roster = mock.Mock()


class SubscribeHandler(webapp2.RequestHandler):
    def post(self):
        # Split the bare XMPP address (e.g., user@gmail.com)
        # from the resource (e.g., gmail), and then add the
        # address to the roster.
        sender = self.request.get("from").split("/")[0]
        roster.add_contact(sender)


class PresenceHandler(webapp2.RequestHandler):
    def post(self):
        # Split the bare XMPP address (e.g., user@gmail.com)
        # from the resource (e.g., gmail), and then add the
        # address to the roster.
        sender = self.request.get("from").split("/")[0]
        xmpp.send_presence(
            sender,
            status=self.request.get("status"),
            presence_show=self.request.get("show"),
        )


class SendPresenceHandler(webapp2.RequestHandler):
    def post(self):
        jid = self.request.get("jid")
        xmpp.send_presence(jid, status="My app's status")


class ErrorHandler(webapp2.RequestHandler):
    def post(self):
        # In the handler for _ah/xmpp/error
        # Log an error
        error_sender = self.request.get("from")
        error_stanza = self.request.get("stanza")
        logging.error(
            "XMPP error received from {} ({})".format(error_sender, error_stanza)
        )


class SendChatHandler(webapp2.RequestHandler):
    def post(self):
        user_address = "example@gmail.com"
        msg = (
            "Someone has sent you a gift on Example.com. "
            "To view: http://example.com/gifts/"
        )
        status_code = xmpp.send_message(user_address, msg)
        chat_message_sent = status_code == xmpp.NO_ERROR

        if not chat_message_sent:
            # Send an email message instead...
            pass


class XMPPHandler(webapp2.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        if message.body[0:5].lower() == "hello":
            message.reply("Greetings!")


app = webapp2.WSGIApplication(
    [
        ("/_ah/xmpp/message/chat/", XMPPHandler),
        ("/_ah/xmpp/subscribe", SubscribeHandler),
        ("/_ah/xmpp/presence/available", PresenceHandler),
        ("/_ah/xmpp/error/", ErrorHandler),
        ("/send_presence", SendPresenceHandler),
        ("/send_chat", SendChatHandler),
    ]
)
