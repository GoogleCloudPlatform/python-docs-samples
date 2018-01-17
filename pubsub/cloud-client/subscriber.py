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
import time

from google.cloud import pubsub_v1


def list_subscriptions_in_topic(project, topic_name):
    """Lists all subscriptions for a given topic."""
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project, topic_name)

    for subscription in subscriber.list_subscriptions(topic_path):
        print(subscription.name)


def list_subscriptions_in_project(project):
    """Lists all subscriptions in the current project."""
    subscriber = pubsub_v1.SubscriberClient()
    project_path = subscriber.project_path(project)

    for subscription in subscriber.list_subscriptions(project_path):
        print(subscription.name)


def create_subscription(project, topic_name, subscription_name):
    """Create a new pull subscription on the given topic."""
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project, topic_name)
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    subscription = subscriber.create_subscription(
        subscription_path, topic_path)

    print('Subscription created: {}'.format(subscription))


def delete_subscription(project, subscription_name):
    """Deletes an existing Pub/Sub topic."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    subscriber.delete_subscription(subscription_path)

    print('Subscription deleted: {}'.format(subscription_path))


def receive_messages(project, subscription_name):
    """Receives messages from a pull subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    def callback(message):
        print('Received message: {}'.format(message))
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)


def receive_messages_with_flow_control(project, subscription_name):
    """Receives messages from a pull subscription with flow control."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    def callback(message):
        print('Received message: {}'.format(message))
        message.ack()

    # Limit the subscriber to only have ten outstanding messages at a time.
    flow_control = pubsub_v1.types.FlowControl(max_messages=10)
    subscriber.subscribe(
        subscription_path, callback=callback, flow_control=flow_control)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)


def listen_for_errors(project, subscription_name):
    """Receives messages and catches errors from a pull subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    def callback(message):
        print('Received message: {}'.format(message))
        message.ack()

    subscription = subscriber.subscribe(subscription_path, callback=callback)

    # Blocks the thread while messages are coming in through the stream. Any
    # exceptions that crop up on the thread will be set on the future.
    try:
        subscription.future.result()
    except Exception as e:
        print(
            'Listening for messages on {} threw an Exception: {}.'.format(
                subscription_name, e))
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('project', help='Your Google Cloud project ID')

    subparsers = parser.add_subparsers(dest='command')
    list_in_topic_parser = subparsers.add_parser(
        'list_in_topic', help=list_subscriptions_in_topic.__doc__)
    list_in_topic_parser.add_argument('topic_name')

    list_in_project_parser = subparsers.add_parser(
        'list_in_project', help=list_subscriptions_in_project.__doc__)

    create_parser = subparsers.add_parser(
        'create', help=create_subscription.__doc__)
    create_parser.add_argument('topic_name')
    create_parser.add_argument('subscription_name')

    delete_parser = subparsers.add_parser(
        'delete', help=delete_subscription.__doc__)
    delete_parser.add_argument('subscription_name')

    receive_parser = subparsers.add_parser(
        'receive', help=receive_messages.__doc__)
    receive_parser.add_argument('subscription_name')

    receive_with_flow_control_parser = subparsers.add_parser(
        'receive-flow-control',
        help=receive_messages_with_flow_control.__doc__)
    receive_with_flow_control_parser.add_argument('subscription_name')

    listen_for_errors_parser = subparsers.add_parser(
        'listen_for_errors', help=listen_for_errors.__doc__)
    listen_for_errors_parser.add_argument('subscription_name')

    args = parser.parse_args()

    if args.command == 'list_in_topic':
        list_subscriptions_in_topic(args.project, args.topic_name)
    elif args.command == 'list_in_project':
        list_subscriptions_in_project(args.project)
    elif args.command == 'create':
        create_subscription(
            args.project, args.topic_name, args.subscription_name)
    elif args.command == 'delete':
        delete_subscription(
            args.project, args.subscription_name)
    elif args.command == 'receive':
        receive_messages(args.project, args.subscription_name)
    elif args.command == 'receive-flow-control':
        receive_messages_with_flow_control(
            args.project, args.subscription_name)
    elif args.command == 'listen_for_errors':
        listen_for_errors(args.project, args.subscription_name)
