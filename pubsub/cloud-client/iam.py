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

"""This application demonstrates how to perform basic operations on IAM
policies with the Cloud Pub/Sub API.

For more information, see the README.md under /pubsub and the documentation
at https://cloud.google.com/pubsub/docs.
"""

import argparse

from google.cloud import pubsub


def get_topic_policy(topic_name):
    """Prints the IAM policy for the given topic."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)

    policy = topic.get_iam_policy()

    print('Policy for topic {}:'.format(topic.name))
    print('Version: {}'.format(policy.version))
    print('Owners: {}'.format(policy.owners))
    print('Editors: {}'.format(policy.editors))
    print('Viewers: {}'.format(policy.viewers))
    print('Publishers: {}'.format(policy.publishers))
    print('Subscribers: {}'.format(policy.subscribers))


def get_subscription_policy(topic_name, subscription_name):
    """Prints the IAM policy for the given subscription."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)
    subscription = topic.subscription(subscription_name)

    policy = subscription.get_iam_policy()

    print('Policy for subscription {} on topic {}:'.format(
        subscription.name, topic.name))
    print('Version: {}'.format(policy.version))
    print('Owners: {}'.format(policy.owners))
    print('Editors: {}'.format(policy.editors))
    print('Viewers: {}'.format(policy.viewers))
    print('Publishers: {}'.format(policy.publishers))
    print('Subscribers: {}'.format(policy.subscribers))


def set_topic_policy(topic_name):
    """Sets the IAM policy for a topic."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)
    policy = topic.get_iam_policy()

    # Add all users as viewers.
    policy.viewers.add(policy.all_users())
    # Add a group as editors.
    policy.editors.add(policy.group('cloud-logs@google.com'))

    # Set the policy
    topic.set_iam_policy(policy)

    print('IAM policy for topic {} set.'.format(topic.name))


def set_subscription_policy(topic_name, subscription_name):
    """Sets the IAM policy for a topic."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)
    subscription = topic.subscription(subscription_name)
    policy = subscription.get_iam_policy()

    # Add all users as viewers.
    policy.viewers.add(policy.all_users())
    # Add a group as editors.
    policy.editors.add(policy.group('cloud-logs@google.com'))

    # Set the policy
    subscription.set_iam_policy(policy)

    print('IAM policy for subscription {} on topic {} set.'.format(
        topic.name, subscription.name))


def check_topic_permissions(topic_name):
    """Checks to which permissions are available on the given topic."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)

    permissions_to_check = [
        'pubsub.topics.publish',
        'pubsub.topics.update'
    ]

    allowed_permissions = topic.check_iam_permissions(permissions_to_check)

    print('Allowed permissions for topic {}: {}'.format(
        topic.name, allowed_permissions))


def check_subscription_permissions(topic_name, subscription_name):
    """Checks to which permissions are available on the given subscription."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)
    subscription = topic.subscription(subscription_name)

    permissions_to_check = [
        'pubsub.subscriptions.consume',
        'pubsub.subscriptions.update'
    ]

    allowed_permissions = subscription.check_iam_permissions(
        permissions_to_check)

    print('Allowed permissions for subscription {} on topic {}: {}'.format(
        subscription.name, topic.name, allowed_permissions))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command')

    get_topic_policy_parser = subparsers.add_parser(
        'get-topic-policy', help=get_topic_policy.__doc__)
    get_topic_policy_parser.add_argument('topic_name')

    get_subscription_policy_parser = subparsers.add_parser(
        'get-subscription-policy', help=get_subscription_policy.__doc__)
    get_subscription_policy_parser.add_argument('topic_name')
    get_subscription_policy_parser.add_argument('subscription_name')

    set_topic_policy_parser = subparsers.add_parser(
        'set-topic-policy', help=set_topic_policy.__doc__)
    set_topic_policy_parser.add_argument('topic_name')

    set_subscription_policy_parser = subparsers.add_parser(
        'set-subscription-policy', help=set_subscription_policy.__doc__)
    set_subscription_policy_parser.add_argument('topic_name')
    set_subscription_policy_parser.add_argument('subscription_name')

    check_topic_permissions_parser = subparsers.add_parser(
        'check-topic-permissions', help=check_topic_permissions.__doc__)
    check_topic_permissions_parser.add_argument('topic_name')

    check_subscription_permissions_parser = subparsers.add_parser(
        'check-subscription-permissions',
        help=check_subscription_permissions.__doc__)
    check_subscription_permissions_parser.add_argument('topic_name')
    check_subscription_permissions_parser.add_argument('subscription_name')

    args = parser.parse_args()

    if args.command == 'get-topic-policy':
        get_topic_policy(args.topic_name)
    elif args.command == 'get-subscription-policy':
        get_subscription_policy(args.topic_name, args.subscription_name)
    elif args.command == 'set-topic-policy':
        set_topic_policy(args.topic_name)
    elif args.command == 'set-subscription-policy':
        set_subscription_policy(args.topic_name, args.subscription_name)
    elif args.command == 'check-topic-permissions':
        check_topic_permissions(args.topic_name)
    elif args.command == 'check-subscription-permissions':
        check_subscription_permissions(args.topic_name, args.subscription_name)
