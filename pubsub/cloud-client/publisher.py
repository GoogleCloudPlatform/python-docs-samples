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

from google.cloud import pubsub_v1


def list_topics(project):
    """Lists all Pub/Sub topics in the given project."""
    publisher = pubsub_v1.PublisherClient()
    project_path = publisher.project_path(project)

    for topic in publisher.list_topics(project_path):
        print(topic)


def create_topic(project, topic_name):
    """Create a new Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)

    topic = publisher.create_topic(topic_path)

    print('Topic created: {}'.format(topic))


def delete_topic(project, topic_name):
    """Deletes an existing Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)

    publisher.delete_topic(topic_path)

    print('Topic deleted: {}'.format(topic_path))


def publish_messages(project, topic_name):
    """Publishes multiple messages to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)

    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        # Data must be a bytestring
        data = data.encode('utf-8')
        publisher.publish(topic_path, data=data)

    print('Published messages.')


def publish_messages_with_futures(project, topic_name):
    """Publishes multiple messages to a Pub/Sub topic and prints their
    message IDs."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)

    # When you publish a message, the client returns a Future. This Future
    # can be used to track when the message is published.
    futures = []

    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        # Data must be a bytestring
        data = data.encode('utf-8')
        message_future = publisher.publish(topic_path, data=data)
        futures.append(message_future)

    print('Published message IDs:')
    for future in futures:
        # result() blocks until the message is published.
        print(future.result())


def publish_messages_with_batch_settings(project, topic_name):
    """Publishes multiple messages to a Pub/Sub topic with batch settings."""
    # Configure the batch to publish once there is one kilobyte of data or
    # 1 second has passed.
    batch_settings = pubsub_v1.types.BatchSettings(
        max_bytes=1024,  # One kilobyte
        max_latency=1,  # One second
    )
    publisher = pubsub_v1.PublisherClient(batch_settings)
    topic_path = publisher.topic_path(project, topic_name)

    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        # Data must be a bytestring
        data = data.encode('utf-8')
        publisher.publish(topic_path, data=data)

    print('Published messages.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('project', help='Your Google Cloud project ID')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('list', help=list_topics.__doc__)

    create_parser = subparsers.add_parser('create', help=create_topic.__doc__)
    create_parser.add_argument('topic_name')

    delete_parser = subparsers.add_parser('delete', help=delete_topic.__doc__)
    delete_parser.add_argument('topic_name')

    publish_parser = subparsers.add_parser(
        'publish', help=publish_messages.__doc__)
    publish_parser.add_argument('topic_name')

    publish_with_futures_parser = subparsers.add_parser(
        'publish-with-futures',
        help=publish_messages_with_futures.__doc__)
    publish_with_futures_parser.add_argument('topic_name')

    publish_with_batch_settings_parser = subparsers.add_parser(
        'publish-with-batch-settings',
        help=publish_messages_with_batch_settings.__doc__)
    publish_with_batch_settings_parser.add_argument('topic_name')

    args = parser.parse_args()

    if args.command == 'list':
        list_topics(args.project)
    elif args.command == 'create':
        create_topic(args.project, args.topic_name)
    elif args.command == 'delete':
        delete_topic(args.project, args.topic_name)
    elif args.command == 'publish':
        publish_messages(args.project, args.topic_name)
    elif args.command == 'publish-with-futures':
        publish_messages_with_futures(args.project, args.topic_name)
    elif args.command == 'publish-with-batch-settings':
        publish_messages_with_batch_settings(args.project, args.topic_name)
