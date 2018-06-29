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
    # [START pubsub_list_topic_subscriptions]
    subscriber = pubsub_v1.PublisherClient()
    topic_path = subscriber.topic_path(project, topic_name)

    for subscription in subscriber.list_topic_subscriptions(topic_path):
        print(subscription)
    # [END pubsub_list_topic_subscriptions]


def list_subscriptions_in_project(project):
    """Lists all subscriptions in the current project."""
    # [START pubsub_list_subscriptions]
    subscriber = pubsub_v1.SubscriberClient()
    project_path = subscriber.project_path(project)

    for subscription in subscriber.list_subscriptions(project_path):
        print(subscription.name)
    # [END pubsub_list_subscriptions]


def create_subscription(project, topic_name, subscription_name):
    """Create a new pull subscription on the given topic."""
    # [START pubsub_create_pull_subscription]
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project, topic_name)
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    subscription = subscriber.create_subscription(
        subscription_path, topic_path)

    print('Subscription created: {}'.format(subscription))
    # [END pubsub_create_pull_subscription]


def create_push_subscription(project,
                             topic_name,
                             subscription_name,
                             endpoint):
    """Create a new push subscription on the given topic."""
    # [START pubsub_create_push_subscription]
    # endpoint = "https://my-test-project.appspot.com/push"
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project, topic_name)
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    push_config = pubsub_v1.types.PushConfig(
        push_endpoint=endpoint)

    subscription = subscriber.create_subscription(
        subscription_path, topic_path, push_config)

    print('Push subscription created: {}'.format(subscription))
    print('Endpoint for subscription is: {}'.format(endpoint))
    # [END pubsub_create_push_subscription]


def delete_subscription(project, subscription_name):
    """Deletes an existing Pub/Sub topic."""
    # [START pubsub_delete_subscription]
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    subscriber.delete_subscription(subscription_path)

    print('Subscription deleted: {}'.format(subscription_path))
    # [END pubsub_delete_subscription]


def update_subscription(project, subscription_name, endpoint):
    """
    Updates an existing Pub/Sub subscription's push endpoint URL.
    Note that certain properties of a subscription, such as
    its topic, are not modifiable.
    """
    # [START pubsub_update_push_configuration]
    # endpoint = "https://my-test-project.appspot.com/push"
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    push_config = pubsub_v1.types.PushConfig(
        push_endpoint=endpoint)

    subscription = pubsub_v1.types.Subscription(
        name=subscription_path,
        push_config=push_config)

    update_mask = {
        'paths': {
            'push_config',
        }
    }

    subscriber.update_subscription(subscription, update_mask)
    result = subscriber.get_subscription(subscription_path)

    print('Subscription updated: {}'.format(subscription_path))
    print('New endpoint for subscription is: {}'.format(
        result.push_config))
    # [END pubsub_update_push_configuration]


def receive_messages(project, subscription_name):
    """Receives messages from a pull subscription."""
    # [START pubsub_subscriber_async_pull]
    # [START pubsub_quickstart_subscriber]
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
    # [END pubsub_subscriber_async_pull]
    # [END pubsub_quickstart_subscriber]


def receive_messages_with_custom_attributes(project, subscription_name):
    """Receives messages from a pull subscription."""
    # [START pubsub_subscriber_sync_pull_custom_attributes]
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    def callback(message):
        print('Received message: {}'.format(message.data))
        if message.attributes:
            print('Attributes:')
            for key in message.attributes:
                value = message.attributes.get(key)
                print('{}: {}'.format(key, value))
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)
    # [END pubsub_subscriber_sync_pull_custom_attributes]


def receive_messages_with_flow_control(project, subscription_name):
    """Receives messages from a pull subscription with flow control."""
    # [START pubsub_subscriber_flow_settings]
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
    # [END pubsub_subscriber_flow_settings]


def listen_for_errors(project, subscription_name):
    """Receives messages and catches errors from a pull subscription."""
    # [START pubsub_subscriber_error_listener]
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
    # [END pubsub_subscriber_error_listener]


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

    create_push_parser = subparsers.add_parser(
        'create-push', help=create_push_subscription.__doc__)
    create_push_parser.add_argument('topic_name')
    create_push_parser.add_argument('subscription_name')
    create_push_parser.add_argument('endpoint')

    delete_parser = subparsers.add_parser(
        'delete', help=delete_subscription.__doc__)
    delete_parser.add_argument('subscription_name')

    update_parser = subparsers.add_parser(
        'update', help=update_subscription.__doc__)
    update_parser.add_argument('subscription_name')
    update_parser.add_argument('endpoint')

    receive_parser = subparsers.add_parser(
        'receive', help=receive_messages.__doc__)
    receive_parser.add_argument('subscription_name')

    receive_with_custom_attributes_parser = subparsers.add_parser(
        'receive-custom-attributes',
        help=receive_messages_with_custom_attributes.__doc__)
    receive_with_custom_attributes_parser.add_argument('subscription_name')

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
    elif args.command == 'create-push':
        create_push_subscription(
            args.project,
            args.topic_name,
            args.subscription_name,
            args.endpoint)
    elif args.command == 'delete':
        delete_subscription(
            args.project, args.subscription_name)
    elif args.command == 'update':
        update_subscription(
            args.project, args.subscription_name, args.endpoint)
    elif args.command == 'receive':
        receive_messages(args.project, args.subscription_name)
    elif args.command == 'receive-custom-attributes':
        receive_messages_with_custom_attributes(
            args.project, args.subscription_name)
    elif args.command == 'receive-flow-control':
        receive_messages_with_flow_control(
            args.project, args.subscription_name)
    elif args.command == 'listen_for_errors':
        listen_for_errors(args.project, args.subscription_name)
