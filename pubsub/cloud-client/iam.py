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

from google.cloud import pubsub_v1


def get_topic_policy(project, topic_name):
    """Prints the IAM policy for the given topic."""
    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(project, topic_name)

    policy = client.get_iam_policy(topic_path)

    print('Policy for topic {}:'.format(topic_path))
    for binding in policy.bindings:
        print('Role: {}, Members: {}'.format(binding.role, binding.members))


def get_subscription_policy(project, subscription_name):
    """Prints the IAM policy for the given subscription."""
    client = pubsub_v1.SubscriberClient()
    subscription_path = client.subscription_path(project, subscription_name)

    policy = client.get_iam_policy(subscription_path)

    print('Policy for subscription {}:'.format(subscription_path))
    for binding in policy.bindings:
        print('Role: {}, Members: {}'.format(binding.role, binding.members))


def set_topic_policy(project, topic_name):
    """Sets the IAM policy for a topic."""
    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(project, topic_name)

    policy = client.get_iam_policy(topic_path)

    # Add all users as viewers.
    policy.bindings.add(
        role='roles/pubsub.viewer',
        members=['allUsers'])

    # Add a group as a publisher.
    policy.bindings.add(
        role='roles/pubsub.publisher',
        members=['group:cloud-logs@google.com'])

    # Set the policy
    policy = client.set_iam_policy(topic_path, policy)

    print('IAM policy for topic {} set: {}'.format(
        topic_name, policy))


def set_subscription_policy(project, subscription_name):
    """Sets the IAM policy for a topic."""
    client = pubsub_v1.SubscriberClient()
    subscription_path = client.subscription_path(project, subscription_name)

    policy = client.get_iam_policy(subscription_path)

    # Add all users as viewers.
    policy.bindings.add(
        role='roles/pubsub.viewer',
        members=['allUsers'])

    # Add a group as an editor.
    policy.bindings.add(
        role='roles/editor',
        members=['group:cloud-logs@google.com'])

    # Set the policy
    policy = client.set_iam_policy(subscription_path, policy)

    print('IAM policy for subscription {} set: {}'.format(
        subscription_name, policy))


def check_topic_permissions(project, topic_name):
    """Checks to which permissions are available on the given topic."""
    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(project, topic_name)

    permissions_to_check = [
        'pubsub.topics.publish',
        'pubsub.topics.update'
    ]

    allowed_permissions = client.test_iam_permissions(
        topic_path, permissions_to_check)

    print('Allowed permissions for topic {}: {}'.format(
        topic_path, allowed_permissions))


def check_subscription_permissions(project, subscription_name):
    """Checks to which permissions are available on the given subscription."""
    client = pubsub_v1.SubscriberClient()
    subscription_path = client.subscription_path(project, subscription_name)

    permissions_to_check = [
        'pubsub.subscriptions.consume',
        'pubsub.subscriptions.update'
    ]

    allowed_permissions = client.test_iam_permissions(
        subscription_path, permissions_to_check)

    print('Allowed permissions for subscription {}: {}'.format(
        subscription_path, allowed_permissions))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('project', help='Your Google Cloud project ID')

    subparsers = parser.add_subparsers(dest='command')

    get_topic_policy_parser = subparsers.add_parser(
        'get-topic-policy', help=get_topic_policy.__doc__)
    get_topic_policy_parser.add_argument('topic_name')

    get_subscription_policy_parser = subparsers.add_parser(
        'get-subscription-policy', help=get_subscription_policy.__doc__)
    get_subscription_policy_parser.add_argument('subscription_name')

    set_topic_policy_parser = subparsers.add_parser(
        'set-topic-policy', help=set_topic_policy.__doc__)
    set_topic_policy_parser.add_argument('topic_name')

    set_subscription_policy_parser = subparsers.add_parser(
        'set-subscription-policy', help=set_subscription_policy.__doc__)
    set_subscription_policy_parser.add_argument('subscription_name')

    check_topic_permissions_parser = subparsers.add_parser(
        'check-topic-permissions', help=check_topic_permissions.__doc__)
    check_topic_permissions_parser.add_argument('topic_name')

    check_subscription_permissions_parser = subparsers.add_parser(
        'check-subscription-permissions',
        help=check_subscription_permissions.__doc__)
    check_subscription_permissions_parser.add_argument('subscription_name')

    args = parser.parse_args()

    if args.command == 'get-topic-policy':
        get_topic_policy(args.project, args.topic_name)
    elif args.command == 'get-subscription-policy':
        get_subscription_policy(args.project, args.subscription_name)
    elif args.command == 'set-topic-policy':
        set_topic_policy(args.project, args.topic_name)
    elif args.command == 'set-subscription-policy':
        set_subscription_policy(args.project, args.subscription_name)
    elif args.command == 'check-topic-permissions':
        check_topic_permissions(args.project, args.topic_name)
    elif args.command == 'check-subscription-permissions':
        check_subscription_permissions(args.project, args.subscription_name)
