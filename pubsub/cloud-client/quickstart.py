#!/usr/bin/env python

# Copyright 2018 Google LLC. All Rights Reserved.
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


import argparse


def end_to_end(project_id, topic_name, subscription_name, num_messages):
    # [START pubsub_quickstart_basic]
    import sys
    import time

    from google.api_core.exceptions import AlreadyExists
    from google.cloud import pubsub_v1
    from google.cloud.pubsub_v1 import types

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"
    # TODO subscription_name = "Your Pub/Sub subscription name"
    # TODO num_messages = number of messages to test end-to-end

    # Instantiates a publisher and subscriber client
    publisher = pubsub_v1.PublisherClient(
        batch_settings=types.BatchSettings(max_messages=1000),)
    subscriber = pubsub_v1.SubscriberClient()

    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_name}`
    topic_path = publisher.topic_path(project_id, topic_name)

    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_name}`
    subscription_path = subscriber.subscription_path(
        project_id, subscription_name)

    # Create the topic.
    try:
        topic = publisher.create_topic(topic_path)
        print('Topic created: {}'.format(topic.name))
    except AlreadyExists:
        print('Topic \"{}\" already exists.'.format(topic_name))

    # Create a subscription.
    try:
        subscription = subscriber.create_subscription(
          subscription_path, topic_path)
        print('Subscription created: {}'.format(subscription.name))
    except AlreadyExists:
        print('Subscription \"{}\" already exists.'.format(subscription_name))

    publish_time = []
    futures = []

    # `data` is roughly 10 Kb
    data = 'x' * 9600
    # Data must be a bytestring
    data = data.encode('utf-8')

    # Publish messages.
    for i in range(num_messages):
        temp = time.time()
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, data=data)
        publish_time.append(time.time() - temp)
        futures.append(future)

    # Time for Pub/Sub to resolve the request and
    # assign a message ID for each message
    resolve_time = []
    for f in futures:
        temp = time.time()
        # `f.result()` is blocking
        f.result()
        resolve_time.append(time.time() - temp)

    messages = set()
    subscribe_time = []

    def callback(message):
        temp = time.time()
        # Unacknowledged messages will be sent again.
        message.ack()
        subscribe_time.append(time.time() - temp)
        messages.add(message)

    # Receive messages. The subscriber is nonblocking.
    subscriber.subscribe(subscription_path, callback=callback)

    print('\nListening for messages on {}...\n'.format(subscription_path))

    while True:
        if len(messages) == num_messages:
            print("Received and acknowledged {} messages.".format(
                num_messages))
            print("Each message is {:.0f}Kb.".format(
                sys.getsizeof(data) / 1.0e3))
            print("They are sent in a batch size of 1000.")
            print("Publish time: {:.6f}s.".format(
                sum(publish_time)+sum(resolve_time)))
            print("Subscribe time: {:.6f}s.".format(sum(subscribe_time)))
            break
        else:
            # Sleeps the thread at 50Hz to save on resources.
            time.sleep(1. / 50)
    # [END pubsub_quickstart_basic]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('project_id', help='Your Google Cloud project ID')

    subparsers = parser.add_subparsers(dest='command')

    basic_parser = subparsers.add_parser('basic', help=end_to_end.__doc__)
    basic_parser.add_argument('topic_name', help='Your topic name')
    basic_parser.add_argument('subscription_name',
                              help='Your subscription name')
    basic_parser.add_argument('num_msgs', type=int,
                              help='Number of test messages')

    args = parser.parse_args()

    if args.command == 'basic':
        end_to_end(args.project_id, args.topic_name, args.subscription_name,
                   args.num_msgs)
