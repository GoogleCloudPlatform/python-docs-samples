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

"""Wikibot server example using SleekXMPP client library"""

import argparse
import getpass
import json
import re
import sys
import urllib

from flask import Flask, request
import requests
from six.moves import html_parser
import sleekxmpp

app = Flask(__name__)


@app.route('/send_message', methods=['GET'])
def send_message():
    recipient = request.args.get('recipient')
    message = request.args.get('message')

    if chat_client and recipient and message:
        chat_client.send_message(mto=recipient, mbody=message)
        return 'message sent to {} with body: {}'.format(recipient, message)
    else:
        return 'message failed to send', 400


class WikiBot(sleekxmpp.ClientXMPP):
    """A simple SleekXMPP bot that will take messages, look up their content on
    wikipedia and provide a link to the page if it exists.
    """

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler('session_start', self.start)

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler('message', self.message)

        # Register plugins. Note that while plugins may have
        # interdependencies, the order you register them in doesn't matter.
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0004')  # Data Forms
        self.register_plugin('xep_0060')  # PubSub
        self.register_plugin('xep_0199')  # XMPP Ping

    def start(self, event):
        """Process the session_start event.

        Typical actions for the session_start event are requesting the roster
        and broadcasting an initial presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start event does not
                provide any additional data.
        """
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        """Process incoming message stanzas.

        Be aware that this also includes MUC messages and error messages. It is
        usually a good idea to check the messages's type before processing or
        sending replies. If the message is the appropriate type, then the bot
        checks wikipedia to see if the message string exists as a page on the
        site. If so, it sends this link back to the sender in the reply.

        Arguments:
            msg -- The received message stanza. See the SleekXMPP documentation
                for stanza objects and the Message stanza to see how it may be
                used.
        """
        if msg['type'] in ('chat', 'normal'):
            msg_body = msg['body']
            encoded_body = urllib.quote_plus(msg_body)
            response = requests.get(
                'https://en.wikipedia.org/w/api.php?'
                'action=query&list=search&format=json&srprop=snippet&'
                'srsearch={}'.format(encoded_body))
            doc = json.loads(response.content)

            results = doc.get('query', {}).get('search')
            if not results:
                msg.reply('I wasn\'t able to locate info on "{}" Sorry'.format(
                    msg_body)).send()
                return

            snippet = results[0]['snippet']
            title = urllib.quote_plus(results[0]['title'])

            # Strip out html
            snippet = html_parser.HTMLParser().unescape(
                re.sub(r'<[^>]*>', '', snippet))
            msg.reply(u'{}...\n(http://en.wikipedia.org/w/?title={})'.format(
                snippet, title)).send()


if __name__ == '__main__':
    # Setup the command line arguments.
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # JID and password options.
    parser.add_argument('-j', '--jid', help='JID to use', required=True)
    parser.add_argument('-p', '--password', help='password to use')

    args = parser.parse_args()

    if args.password is None:
        args.password = getpass.getpass('Password: ')

    xmpp = WikiBot(args.jid, args.password)

    chat_client = xmpp  # set the global variable

    try:
        # Connect to the XMPP server and start processing XMPP stanzas.
        if not xmpp.connect():
            print('Unable to connect.')
            sys.exit(1)

        xmpp.process(block=False)

        app.run(threaded=True, use_reloader=False, host='0.0.0.0', debug=False)
        print('Done')
    finally:
        xmpp.disconnect()
