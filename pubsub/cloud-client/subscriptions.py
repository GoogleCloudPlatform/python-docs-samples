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
subscriptions with the Google Cloud Pub/Sub API.

For more information, see the README.md under /pubsub and the documentation at
https://cloud.google.com/pubsub/docs.
"""

import argparse
import os

from google.cloud import pubsub


pubsub_client = pubsub.Client()


# [START pubsub_list_subscriptions]
def list_subscriptions():
    # Lists all subscriptions in the current project
    subscriptions = []
    next_page_token = None
    while True:
        page, next_page_token = pubsub_client.list_subscriptions()
        subscriptions.extend(page)
        if not next_page_token:
            break

    print('Subscriptions:')
    for subscription in subscriptions:
        print(subscription.name)
# [END pubsub_list_subscriptions]


# [START pubsub_list_topic_subscriptions]
def list_topic_subscriptions(topic_name):
    # Reference an existing topic, e.g. "my-topic"
    topic = pubsub_client.topic(topic_name)

    # Lists all subscriptions for the topic
    subscriptions = []
    next_page_token = None
    while True:
        page, next_page_token = topic.list_subscriptions()
        subscriptions.extend(page)
        if not next_page_token:
            break

    print('Subscriptions:')
    for subscription in subscriptions:
        print(subscription.name)
# [END pubsub_list_topic_subscriptions]


# [START pubsub_create_subscription]
def create_subscription(topic_name, subscription_name):
    # References an existing topic, e.g. "my-topic"
    topic = pubsub_client.topic(topic_name)

    # Prepares a new subscription, e.g. "my-new-subscription"
    subscription = topic.subscription(subscription_name)

    # Creates the subscription
    subscription.create()

    print('Subscription {} created.'.format(subscription.name))
# [END pubsub_create_subscription]


# [START pubsub_create_push_subscription]
def create_push_subscription(topic_name, subscription_name):
    # References an existing topic, e.g. "my-topic"
    topic = pubsub_client.topic(topic_name)

    project_id = os.environ['GCLOUD_PROJECT'] or 'YOUR_PROJECT_ID'

    # Prepares a new push subscription, e.g. "my-new-subscription"
    subscription = topic.subscription(
        subscription_name,
        # Set to an HTTPS endpoint of your choice. If necessary, register
        # (authorize) the domain on which the server is hosted.
        push_endpoint = 'https://{}.appspot.com/push'.format(project_id)
    )

    # Creates the push subscription
    subscription.create()

    print('Subscription {} created.'.format(subscription.name))
# [END pubsub_create_push_subscription]


# [START pubsub_delete_subscription]
def delete_subscription(topic_name, subscription_name):
    # References an existing topic, e.g. "my-topic"
    topic = pubsub_client.topic(topic_name)

    # References an existing subscription, e.g. "my-subscription"
    subscription = topic.subscription(subscription_name)

    # Deletes the subscription
    subscription.delete()

    print('Subscription {} deleted.'.format(subscription.name))
# [END pubsub_delete_subscription]


# [START pubsub_get_subscription_metadata]
def get_subscription_metadata(topic_name, subscription_name):
    # References an existing topic, e.g. "my-topic"
    topic = pubsub_client.topic(topic_name)

    # References an existing subscription, e.g. "my-subscription"
    subscription = topic.subscription(subscription_name)

    # Gets the metadata for the subscription
    subscription.reload()

    print('Subscription: {}'.format(subscription.name))
    print('Topic: {}'.format(subscription.topic.name))
    print('Push config: {}'.format(subscription.push_endpoint))
    print('Ack deadline: {}s'.format(subscription.ack_deadline))
# [END pubsub_get_subscription_metadata]


# [START pubsub_pull_messages]
def pull_messages(topic_name, subscription_name):
    # References an existing topic, e.g. "my-topic"
    topic = pubsub_client.topic(topic_name)

    # References an existing subscription, e.g. "my-subscription"
    subscription = topic.subscription(subscription_name)

    # Pulls messages. Set return_immediately to False to block until messages
    # are received.
    results = subscription.pull(return_immediately=True)

    print('Received {} messages.'.format(len(results)))

    for message in results:
        print('* {}: {}, {}'.format(
            message.message_id, message.data, message.attributes))

    # Acknowledges received messages. If you do not acknowledge, Pub/Sub will
    # redeliver the message.
    if results:
        subscription.acknowledge([ack_id for ack_id, message in results])
# [END pubsub_pull_messages]


# [START pubsub_get_subscription_policy]
def get_subscription_policy(topic_name, subscription_name):
    # References an existing topic, e.g. "my-topic"
    topic = pubsub_client.topic(topic_name)

    # References an existing subscription, e.g. "my-subscription"
    subscription = topic.subscription(subscription_name)

    # Retrieves the IAM policy for the subscription
    policy = subscription.get_iam_policy()

    print('Policy for subscription: {}'.format(policy.to_api_repr()))
# [END pubsub_get_subscription_policy]


# [START pubsub_set_subscription_policy]
def set_subscription_policy(topic_name, subscription_name):
    # References an existing topic, e.g. "my-topic"
    topic = pubsub_client.topic(topic_name)

    # References an existing subscription, e.g. "my-subscription"
    subscription = topic.subscription(subscription_name)

    # Retrieves the IAM policy for the subscription
    policy = subscription.get_iam_policy()

    # Add all users as viewers
    policy.viewers.add(policy.all_users())
    # Add a group as editors
    policy.editors.add(policy.group('cloud-logs@google.com'))

    # Updates the IAM policy for the subscription
    subscription.set_iam_policy(policy)

    print('Updated policy for subscription: {}.'.format(policy.to_api_repr()))
# [END pubsub_set_subscription_policy]


# [START pubsub_test_subscription_permissions]
def test_subscription_permissions(topic_name, subscription_name):
    # References an existing topic, e.g. "my-new-topic"
    topic = pubsub_client.topic(topic_name)

    # References an existing subscription, e.g. "my-subscription"
    subscription = topic.subscription(subscription_name)

    permissions_to_test = [
        'pubsub.subscriptions.consume',
        'pubsub.subscriptions.update'
    ]

    # Tests the IAM policy for the subscripti
    allowed_permissions = subscription.check_iam_permissions(
        permissions_to_test)

    print('Tested permissions for subscription: {}'.format(allowed_permissions))
# [END pubsub_test_subscription_permissions]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command')
    list_parser = subparsers.add_parser(
        'list', help=list_subscriptions.__doc__)
    list_parser.add_argument('topic_name', nargs='?')

    create_parser = subparsers.add_parser(
        'create', help=create_subscription.__doc__)
    create_parser.add_argument('topic_name')
    create_parser.add_argument('subscription_name')

    create_push_parser = subparsers.add_parser(
        'create-push', help=create_push_subscription.__doc__)
    create_push_parser.add_argument('topic_name')
    create_push_parser.add_argument('subscription_name')

    delete_parser = subparsers.add_parser(
        'delete', help=delete_subscription.__doc__)
    delete_parser.add_argument('topic_name')
    delete_parser.add_argument('subscription_name')

    get_parser = subparsers.add_parser(
        'get', help=get_subscription_metadata.__doc__)
    get_parser.add_argument('topic_name')
    get_parser.add_argument('subscription_name')

    receive_parser = subparsers.add_parser(
        'receive', help=pull_messages.__doc__)
    receive_parser.add_argument('topic_name')
    receive_parser.add_argument('subscription_name')

    get_policy_parser = subparsers.add_parser(
        'get-policy', help=get_subscription_policy.__doc__)
    get_policy_parser.add_argument('topic_name')
    get_policy_parser.add_argument('subscription_name')

    set_policy_parser = subparsers.add_parser(
        'set-policy', help=set_subscription_policy.__doc__)
    set_policy_parser.add_argument('topic_name')
    set_policy_parser.add_argument('subscription_name')

    test_permissions_parser = subparsers.add_parser(
        'test-permissions', help=test_subscription_permissions.__doc__)
    test_permissions_parser.add_argument('topic_name')
    test_permissions_parser.add_argument('subscription_name')

    args = parser.parse_args()

    if args.command == 'list':
        if args.topic_name:
            list_topic_subscriptions(args.topic_name)
        else:
            list_subscriptions()
    elif args.command == 'create':
        create_subscription(args.topic_name, args.subscription_name)
    elif args.command == 'create-push':
        create_push_subscription(args.topic_name, args.subscription_name)
    elif args.command == 'delete':
        delete_subscription(args.topic_name, args.subscription_name)
    elif args.command == 'get':
        get_subscription_metadata(args.topic_name, args.subscription_name)
    elif args.command == 'receive':
        pull_messages(args.topic_name, args.subscription_name)
    elif args.command == 'get-policy':
        get_subscription_policy(args.topic_name, args.subscription_name)
    elif args.command == 'set-policy':
        set_subscription_policy(args.topic_name, args.subscription_name)
    elif args.command == 'test-permissions':
        test_subscription_permissions(args.topic_name, args.subscription_name)
