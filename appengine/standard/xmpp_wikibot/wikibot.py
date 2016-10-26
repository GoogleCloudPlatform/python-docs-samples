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

import json
import logging
from optparse import OptionParser
import sys
import threading
import urllib

from flask import Flask, request
import requests
import sleekxmpp

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input

app = Flask(__name__)

chat_client = None #this will be initialized when the wikibot is constructed

@app.route('/send_message', methods=['GET'])
def send_message():
    try:
        recipient = request.args.get('recipient')
        message = request.args.get('message')
    except KeyError as e:
        logging.info('key error: {0}'.format(e))

    if chat_client and recipient and message:
        chat_client.send_message(mto=recipient, mbody=message)
        return 'message sent to:' + recipient + ' with body:' + message
    else:
        logging.info('chat client or recipient or message does not exist!')
    return 'message failed to send'

def run_server():
    app.run(threaded=False, use_reloader=False, host='0.0.0.0')

class WikiBot(sleekxmpp.ClientXMPP):

    """
    A simple SleekXMPP bot that will take messages, look up their content
    on wikipedia and provide a link to the page if it exists
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

    def start(self, event):
        """
        Process the session_start event.
        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.
        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies. If the message is the appropriate type,
        then the bot checks wikipedia to see if the message string
        exists as a page on the site. If so, it sends this link back
        to the sender in the reply.
        Arguments:
            msg -- The received message stanza. See the SleekXMPP documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['type'] in ('chat', 'normal'):
            msg_body = '%(body)s' % msg
            logging.info('Message sent was: ' + msg_body)
            encoded_body = urllib.quote_plus(msg_body)
            svrResponse = requests.get('https://en.wikipedia.org/w/api.php?action=parse&prop=sections&format=json&page=' + encoded_body)
            doc = json.loads(svrResponse.content)
            try:
                page_id = str(doc['parse']['pageid'])
                defn_url = 'https://en.wikipedia.org/?curid=' + page_id
                msg.reply("find out more about: '" + msg_body + "' here: " + defn_url).send()
            except KeyError as e:
                logging.info('key error: {0}'.format(e))
                msg.reply("I wasn't able to locate info on: '" + msg_body + "' Sorry").send()




if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')


    # Setup the WikiBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = WikiBot(opts.jid, opts.password)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping

    chat_client = xmpp # set the global variable

    # If you are connecting to Facebook and wish to use the
    # X-FACEBOOK-PLATFORM authentication mechanism, you will need
    # your API key and an access token. Then you'll set:
    # xmpp.credentials['api_key'] = 'THE_API_KEY'
    # xmpp.credentials['access_token'] = 'THE_ACCESS_TOKEN'

    # If you are connecting to MSN, then you will need an
    # access token, and it does not matter what JID you
    # specify other than that the domain is 'messenger.live.com',
    # so '_@messenger.live.com' will work. You can specify
    # the access token as so:
    # xmpp.credentials['access_token'] = 'THE_ACCESS_TOKEN'

    # If you are working with an OpenFire server, you may need
    # to adjust the SSL version used:
    # xmpp.ssl_version = ssl.PROTOCOL_SSLv3

    # If you want to verify the SSL certificates offered by a server:
    # xmpp.ca_certs = "path/to/ca/cert"

    # start the app server and run it as a thread so that the XMPP server may also start
    threading.Thread(target=run_server).start()

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example:
        #
        # if xmpp.connect(('<SERVER DOMAIN>.com', 5222)):
        #     ...
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")