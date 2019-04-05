# Copyright 2018 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os

from datetime import datetime
from flask import Flask
from googleapiclient.discovery import build
from google.appengine.api import app_identity
from time import sleep


APP = Flask(__name__)

SUBSCRIPTION_AGGREGATED = os.environ['PUBSUB_SUBSCRIPTION_AGGREGATED']
SUBSCRIPTION_SINGLE = os.environ['PUBSUB_SUBSCRIPTION_SINGLE']
TOPIC_FORWARD = os.environ['PUBSUB_TOPIC_FORWARD']

CRON_MINUTES = os.environ['CRON_MINUTES']
MAX_MESSAGES = os.environ['MAX_MESSAGES']
WAIT_TIME = 1 / float(os.getenv('QPS', '1000'))

PROJECT = app_identity.get_application_id()

service = build('pubsub', 'v1')


@APP.route('/pull-forward-findings', methods=['GET'])
def index():
    start_time = datetime.now()
    logging.debug('Started at {}'.format(unicode(start_time)))

    forward_topic = 'projects/{}/topics/{}'.format(PROJECT, TOPIC_FORWARD)
    subscriptions = [
        'projects/{}/subscriptions/{}'.format(PROJECT, SUBSCRIPTION_AGGREGATED),
        'projects/{}/subscriptions/{}'.format(PROJECT, SUBSCRIPTION_SINGLE)
    ]

    currentSub = 0
    messagesSent = 0
    while hasEnoughTime(start_time):
        # restart counter for messages sent within current loop
        if currentSub == 0:
            messagesSent = 0

        # forward messages from current subscription
        messagesSent += forwardMessages(subscriptions[currentSub], forward_topic)

        # check if at least one message was sent within current loop
        if currentSub == len(subscriptions) - 1 and messagesSent == 0:
            # no messages to forward, stop current loop
            logging.debug('No messages to forward')
            break

        # get next subscription
        currentSub = (currentSub + 1) % len(subscriptions)

    # log finish
    logging.debug('Finished at {}'.format(unicode(datetime.now())))

    # execution complete
    return 'OK', 200


def hasEnoughTime(start_time):
    # check if there is at least 20% time remaining from CRON_MINUTES since the begining of the script
    return (datetime.now() - start_time).seconds < float(CRON_MINUTES) * 60 * 0.8


def forwardMessages(subscription, forward_topic):
    # get MAX_MESSAGES from subscription
    logging.debug('Pulling messages from subscription: {}'.format(subscription))
    pull_response = service.projects().subscriptions().pull(
        subscription = subscription,
        body = {
            'maxMessages': float(MAX_MESSAGES),
            'returnImmediately': True
        }
    ).execute()

    # save ids from received messages to send ack
    ack_ids = []

    # check received messages
    if 'receivedMessages' in pull_response:
        logging.debug('{} message(s) received'.format(len(pull_response['receivedMessages'])))

        # forward messages to forward topic
        for pub_sub_message in pull_response['receivedMessages']:
            # forwarding message
            logging.debug('Forwarding message {} to topic: {}'.format(pub_sub_message['message']['messageId'], forward_topic))
            service.projects().topics().publish(
                topic = forward_topic,
                body = {
                    'messages': [{
                        'data': pub_sub_message['message']['data']
                    }]
                }).execute()

            # saving id to ack
            ack_ids.append(pub_sub_message['ackId'])

            # throttle
            sleep(WAIT_TIME)

        # acknowledging messages received
        logging.debug('Acknowledging ids: {}'.format(ack_ids))
        service.projects().subscriptions().acknowledge(
            subscription = subscription,
            body = {
                'ackIds': ack_ids
            }
        ).execute()
    else:
        logging.debug('0 messages received')

    # return amount of messages forwarded
    return len(ack_ids)


@APP.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    APP.run(host='127.0.0.1', port=8080, debug=True)
