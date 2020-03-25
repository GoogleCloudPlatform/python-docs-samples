#!/usr/bin/env python

# Copyright 2016 Google LLC. All Rights Reserved.
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


def list_topics(project_id):
    """Lists all Pub/Sub topics in the given project."""
    # [START pubsub_list_topics]
    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"

    publisher = pubsub_v1.PublisherClient()
    project_path = publisher.project_path(project_id)

    for topic in publisher.list_topics(project_path):
        print(topic)
    # [END pubsub_list_topics]


def create_topic(project_id, topic_name):
    """Create a new Pub/Sub topic."""
    # [START pubsub_quickstart_create_topic]
    # [START pubsub_create_topic]
    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    topic = publisher.create_topic(topic_path)

    print("Topic created: {}".format(topic))
    # [END pubsub_quickstart_create_topic]
    # [END pubsub_create_topic]


def delete_topic(project_id, topic_name):
    """Deletes an existing Pub/Sub topic."""
    # [START pubsub_delete_topic]
    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    publisher.delete_topic(topic_path)

    print("Topic deleted: {}".format(topic_path))
    # [END pubsub_delete_topic]


def publish_messages(project_id, topic_name):
    """Publishes multiple messages to a Pub/Sub topic."""
    # [START pubsub_quickstart_publisher]
    # [START pubsub_publish]
    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"

    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_name}`
    topic_path = publisher.topic_path(project_id, topic_name)

    for n in range(1, 10):
        data = u"Message number {}".format(n)
        # Data must be a bytestring
        data = data.encode("utf-8")
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, data=data)
        print(future.result())

    print("Published messages.")
    # [END pubsub_quickstart_publisher]
    # [END pubsub_publish]


def publish_messages_with_custom_attributes(project_id, topic_name):
    """Publishes multiple messages with custom attributes
    to a Pub/Sub topic."""
    # [START pubsub_publish_custom_attributes]
    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    for n in range(1, 10):
        data = u"Message number {}".format(n)
        # Data must be a bytestring
        data = data.encode("utf-8")
        # Add two attributes, origin and username, to the message
        future = publisher.publish(
            topic_path, data, origin="python-sample", username="gcp"
        )
        print(future.result())

    print("Published messages with custom attributes.")
    # [END pubsub_publish_custom_attributes]


def publish_messages_with_error_handler(project_id, topic_name):
    # [START pubsub_publish_messages_error_handler]
    """Publishes multiple messages to a Pub/Sub topic with an error handler."""
    import time

    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    futures = dict()

    def get_callback(f, data):
        def callback(f):
            try:
                print(f.result())
                futures.pop(data)
            except:  # noqa
                print("Please handle {} for {}.".format(f.exception(), data))

        return callback

    for i in range(10):
        data = str(i)
        futures.update({data: None})
        # When you publish a message, the client returns a future.
        future = publisher.publish(
            topic_path, data=data.encode("utf-8")  # data must be a bytestring.
        )
        futures[data] = future
        # Publish failures shall be handled in the callback function.
        future.add_done_callback(get_callback(future, data))

    # Wait for all the publish futures to resolve before exiting.
    while futures:
        time.sleep(5)

    print("Published message with error handler.")
    # [END pubsub_publish_messages_error_handler]


def publish_messages_with_batch_settings(project_id, topic_name):
    """Publishes multiple messages to a Pub/Sub topic with batch settings."""
    # [START pubsub_publisher_batch_settings]
    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"

    # Configure the batch to publish as soon as there is ten messages,
    # one kilobyte of data, or one second has passed.
    batch_settings = pubsub_v1.types.BatchSettings(
        max_messages=10,  # default 100
        max_bytes=1024,  # default 1 MB
        max_latency=1,  # default 10 ms
    )
    publisher = pubsub_v1.PublisherClient(batch_settings)
    topic_path = publisher.topic_path(project_id, topic_name)

    # Resolve the publish future in a separate thread.
    def callback(future):
        message_id = future.result()
        print(message_id)

    for n in range(1, 10):
        data = u"Message number {}".format(n)
        # Data must be a bytestring
        data = data.encode("utf-8")
        future = publisher.publish(topic_path, data=data)
        # Non-blocking. Allow the publisher client to batch multiple messages.
        future.add_done_callback(callback)

    print("Published messages with batch settings.")
    # [END pubsub_publisher_batch_settings]


def publish_messages_with_retry_settings(project_id, topic_name):
    """Publishes messages with custom retry settings."""
    # [START pubsub_publisher_retry_settings]
    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"

    # Configure the retry settings. Defaults will be overwritten.
    retry_settings = {
        "interfaces": {
            "google.pubsub.v1.Publisher": {
                "retry_codes": {
                    "publish": [
                        "ABORTED",
                        "CANCELLED",
                        "DEADLINE_EXCEEDED",
                        "INTERNAL",
                        "RESOURCE_EXHAUSTED",
                        "UNAVAILABLE",
                        "UNKNOWN",
                    ]
                },
                "retry_params": {
                    "messaging": {
                        "initial_retry_delay_millis": 100,  # default: 100
                        "retry_delay_multiplier": 1.3,  # default: 1.3
                        "max_retry_delay_millis": 60000,  # default: 60000
                        "initial_rpc_timeout_millis": 5000,  # default: 25000
                        "rpc_timeout_multiplier": 1.0,  # default: 1.0
                        "max_rpc_timeout_millis": 600000,  # default: 30000
                        "total_timeout_millis": 600000,  # default: 600000
                    }
                },
                "methods": {
                    "Publish": {
                        "retry_codes_name": "publish",
                        "retry_params_name": "messaging",
                    }
                },
            }
        }
    }

    publisher = pubsub_v1.PublisherClient(client_config=retry_settings)
    topic_path = publisher.topic_path(project_id, topic_name)

    for n in range(1, 10):
        data = u"Message number {}".format(n)
        # Data must be a bytestring
        data = data.encode("utf-8")
        future = publisher.publish(topic_path, data=data)
        print(future.result())

    print("Published messages with retry settings.")
    # [END pubsub_publisher_retry_settings]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID")

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help=list_topics.__doc__)

    create_parser = subparsers.add_parser("create", help=create_topic.__doc__)
    create_parser.add_argument("topic_name")

    delete_parser = subparsers.add_parser("delete", help=delete_topic.__doc__)
    delete_parser.add_argument("topic_name")

    publish_parser = subparsers.add_parser(
        "publish", help=publish_messages.__doc__
    )
    publish_parser.add_argument("topic_name")

    publish_with_custom_attributes_parser = subparsers.add_parser(
        "publish-with-custom-attributes",
        help=publish_messages_with_custom_attributes.__doc__,
    )
    publish_with_custom_attributes_parser.add_argument("topic_name")

    publish_with_error_handler_parser = subparsers.add_parser(
        "publish-with-error-handler",
        help=publish_messages_with_error_handler.__doc__,
    )
    publish_with_error_handler_parser.add_argument("topic_name")

    publish_with_batch_settings_parser = subparsers.add_parser(
        "publish-with-batch-settings",
        help=publish_messages_with_batch_settings.__doc__,
    )
    publish_with_batch_settings_parser.add_argument("topic_name")

    publish_with_retry_settings_parser = subparsers.add_parser(
        "publish-with-retry-settings",
        help=publish_messages_with_retry_settings.__doc__,
    )
    publish_with_retry_settings_parser.add_argument("topic_name")

    args = parser.parse_args()

    if args.command == "list":
        list_topics(args.project_id)
    elif args.command == "create":
        create_topic(args.project_id, args.topic_name)
    elif args.command == "delete":
        delete_topic(args.project_id, args.topic_name)
    elif args.command == "publish":
        publish_messages(args.project_id, args.topic_name)
    elif args.command == "publish-with-custom-attributes":
        publish_messages_with_custom_attributes(
            args.project_id, args.topic_name
        )
    elif args.command == "publish-with-error-handler":
        publish_messages_with_error_handler(args.project_id, args.topic_name)
    elif args.command == "publish-with-batch-settings":
        publish_messages_with_batch_settings(args.project_id, args.topic_name)
    elif args.command == "publish-with-retry-settings":
        publish_messages_with_retry_settings(args.project_id, args.topic_name)
