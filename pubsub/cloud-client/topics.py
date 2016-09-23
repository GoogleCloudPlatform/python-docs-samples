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

"""This application demonstrates how to perform basic operations on topics
with the Google Cloud Pub/Sub API.

For more information, see the README.md under /pubsub and the documentation at
https://cloud.google.com/pubsub/docs.
"""

import argparse

from google.cloud import pubsub


pubsub_client = pubsub.Client()


# [START pubsub_list_topics]
def list_topics():
    # Lists all topics in the current project
    topics = []
    next_page_token = None
    while True:
        page, next_page_token = pubsub_client.list_topics()
        topics.extend(page)
        if not next_page_token:
            break

    print('Topics:')
    for topic in topics:
        print(topic.name)
# [END pubsub_list_topics]


# [START pubsub_create_topic]
def create_topic(topic_name):
    # Prepares a topic instance, e.g. "my-new-topic"
    topic = pubsub_client.topic(topic_name)

    # Creates the new topic
    topic.create()

    print('Topic {} created.'.format(topic.name))
# [END pubsub_create_topic]


# [START pubsub_delete_topic]
def delete_topic(topic_name):
    # References an existing topic, e.g. "my-new-topic"
    topic = pubsub_client.topic(topic_name)

    # Deletes the topic
    topic.delete()

    print('Topic {} deleted.'.format(topic.name))
# [END pubsub_delete_topic]


# [START pubsub_publish_message]
def publish_message(topic_name, data):
    # References an existing topic, e.g. "my-new-topic"
    topic = pubsub_client.topic(topic_name)

    # Data must be a bytestring
    data = data.encode('utf-8')

    # Publishes the message
    message_id = topic.publish(data)

    print('Message {} published.'.format(message_id))
# [END pubsub_publish_message]


# [START pubsub_get_topic_policy]
def get_topic_policy(topic_name):
    # References an existing topic, e.g. "my-new-topic"
    topic = pubsub_client.topic(topic_name)

    # Retrieves the IAM policy for the topic
    policy = topic.get_iam_policy()

    print('Policy for topic: {}'.format(policy.to_api_repr()))
# [END pubsub_get_topic_policy]


# [START pubsub_set_topic_policy]
def set_topic_policy(topic_name):
    # References an existing topic, e.g. "my-new-topic"
    topic = pubsub_client.topic(topic_name)

    # Retrieves the IAM policy for the topic
    policy = topic.get_iam_policy()

    # Add all users as viewers
    policy.viewers.add(policy.all_users())
    # Add a group as editors
    policy.editors.add(policy.group('cloud-logs@google.com'))

    # Updates the IAM policy for the topic
    topic.set_iam_policy(policy)

    print('Updated policy for topic: {}.'.format(policy.to_api_repr()))
# [END pubsub_set_topic_policy]


# [START pubsub_test_topic_permissions]
def test_topic_permissions(topic_name):
    # References an existing topic, e.g. "my-new-topic"
    topic = pubsub_client.topic(topic_name)

    permissions_to_test = [
        'pubsub.topics.attachSubscription',
        'pubsub.topics.publish',
        'pubsub.topics.update'
    ]

    # Tests the IAM policy for the topic
    allowed_permissions = topic.check_iam_permissions(permissions_to_test)

    print('Tested permissions for topic: {}'.format(allowed_permissions))
# [END pubsub_test_topic_permissions]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('list', help=list_topics.__doc__)

    create_parser = subparsers.add_parser('create', help=create_topic.__doc__)
    create_parser.add_argument('topic_name')

    delete_parser = subparsers.add_parser('delete', help=delete_topic.__doc__)
    delete_parser.add_argument('topic_name')

    publish_parser = subparsers.add_parser(
        'publish', help=publish_message.__doc__)
    publish_parser.add_argument('topic_name')
    publish_parser.add_argument('data')

    get_policy_parser = subparsers.add_parser(
        'get-policy', help=delete_topic.__doc__)
    get_policy_parser.add_argument('topic_name')

    set_policy_parser = subparsers.add_parser(
        'set-policy', help=delete_topic.__doc__)
    set_policy_parser.add_argument('topic_name')

    test_permissions_parser = subparsers.add_parser('
        test-permissions', help=delete_topic.__doc__)
    test_permissions_parser.add_argument('topic_name')

    args = parser.parse_args()

    if args.command == 'list':
        list_topics()
    elif args.command == 'create':
        create_topic(args.topic_name)
    elif args.command == 'delete':
        delete_topic(args.topic_name)
    elif args.command == 'publish':
        publish_message(args.topic_name, args.data)
    elif args.command == 'get-policy':
        get_topic_policy(args.topic_name)
    elif args.command == 'set-policy':
        set_topic_policy(args.topic_name)
    elif args.command == 'test-permissions':
        test_topic_permissions(args.topic_name)
