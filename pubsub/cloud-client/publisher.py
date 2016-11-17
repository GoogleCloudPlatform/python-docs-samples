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
with the Cloud Pub/Sub API.

For more information, see the README.md under /pubsub and the documentation
at https://cloud.google.com/pubsub/docs.
"""

import argparse

from google.cloud import pubsub


def list_topics():
    """Lists all Pub/Sub topics in the current project."""
    pubsub_client = pubsub.Client()

    for topic in pubsub_client.list_topics():
        print(topic.name)


def create_topic(topic_name):
    """Create a new Pub/Sub topic."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)

    topic.create()

    print('Topic {} created.'.format(topic.name))


def delete_topic(topic_name):
    """Deletes an existing Pub/Sub topic."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)

    topic.delete()

    print('Topic {} deleted.'.format(topic.name))


def publish_message(topic_name, data):
    """Publishes a message to a Pub/Sub topic with the given data."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)

    # Data must be a bytestring
    data = data.encode('utf-8')

    message_id = topic.publish(data)

    print('Message {} published.'.format(message_id))


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

    args = parser.parse_args()

    if args.command == 'list':
        list_topics()
    elif args.command == 'create':
        create_topic(args.topic_name)
    elif args.command == 'delete':
        delete_topic(args.topic_name)
    elif args.command == 'publish':
        publish_message(args.topic_name, args.data)
