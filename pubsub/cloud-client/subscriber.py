#!/usr/bin/env python

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

"""This application demonstrates how to perform basic operations on
subscriptions with the Cloud Pub/Sub API.

For more information, see the README.md under /pubsub and the documentation
at https://cloud.google.com/pubsub/docs.
"""

import argparse

from google.cloud import pubsub


def list_subscriptions(topic_name):
    """Lists all subscriptions for a given topic."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)

    for subscription in topic.list_subscriptions():
        print(subscription.name)


def create_subscription(topic_name, subscription_name):
    """Create a new pull subscription on the given topic."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)

    subscription = topic.subscription(subscription_name)
    subscription.create()

    print('Subscription {} created on topic {}.'.format(
        subscription.name, topic.name))


def delete_subscription(topic_name, subscription_name):
    """Deletes an existing Pub/Sub topic."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)
    subscription = topic.subscription(subscription_name)

    subscription.delete()

    print('Subscription {} deleted on topic {}.'.format(
        subscription.name, topic.name))


def receive_message(topic_name, subscription_name):
    """Receives a message from a pull subscription."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)
    subscription = topic.subscription(subscription_name)

    # Change return_immediately=False to block until messages are
    # received.
    results = subscription.pull(return_immediately=True)

    print('Received {} messages.'.format(len(results)))

    for ack_id, message in results:
        print('* {}: {}, {}'.format(
            message.message_id, message.data, message.attributes))

    # Acknowledge received messages. If you do not acknowledge, Pub/Sub will
    # redeliver the message.
    if results:
        subscription.acknowledge([ack_id for ack_id, message in results])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command')
    list_parser = subparsers.add_parser(
        'list', help=list_subscriptions.__doc__)
    list_parser.add_argument('topic_name')

    create_parser = subparsers.add_parser(
        'create', help=create_subscription.__doc__)
    create_parser.add_argument('topic_name')
    create_parser.add_argument('subscription_name')

    delete_parser = subparsers.add_parser(
        'delete', help=delete_subscription.__doc__)
    delete_parser.add_argument('topic_name')
    delete_parser.add_argument('subscription_name')

    receive_parser = subparsers.add_parser(
        'receive', help=receive_message.__doc__)
    receive_parser.add_argument('topic_name')
    receive_parser.add_argument('subscription_name')

    args = parser.parse_args()

    if args.command == 'list':
        list_subscriptions(args.topic_name)
    elif args.command == 'create':
        create_subscription(args.topic_name, args.subscription_name)
    elif args.command == 'delete':
        delete_subscription(args.topic_name, args.subscription_name)
    elif args.command == 'receive':
        receive_message(args.topic_name, args.subscription_name)
