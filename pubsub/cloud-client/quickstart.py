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


def end_to_end(project_id, topic_name, subscription_name):
    # [START pubsub_end_to_end]
    import time

    from google.api_core.exceptions import NotFound
    from google.cloud import pubsub_v1

    def create_topic_safely(publisher, topic_path):
        try:
            publisher.delete_topic(topic_path)
        except NotFound:
            pass

        topic = publisher.create_topic(topic_path)
        print('Topic created: \"{}\"'.format(topic.name))

    def create_subscription_safely(subscriber, subscription_path):
        try:
            subscriber.delete_subscription(subscription_path)
        except NotFound:
            pass

        subscription = subscriber.create_subscription(
            subscription_path, topic_path)
        print('Subscription created: \"{}\"'.format(subscription.name))

    # TODO project_id = "Your Pub/Sub project id"
    # TODO topic_name = "Your Pub/Sub topic name"
    # TODO subscription_name = "Your Pub/Sub subscription name"

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(
        project_id, subscription_name)

    create_topic_safely(publisher, topic_path)
    create_subscription_safely(subscriber, subscription_path)

    # `data` must be a bytestring.
    data = 'x' * 10000
    data = data.encode('utf-8')
    # Initialize an empty dictionary to track messages.
    tracker = dict()
    delivery_times = []
    num_messages = 10

    def resolve_future_callback(future):
        """Resolve the publish future and update `tracker` asynchronously."""
        pubtime = time.time()
        message_id = future.result()
        tracker.update({message_id: {'pubtime': pubtime, 'subtime': None}})

    def publish_messages(publish_func, callback):
        for i in range(num_messages):
            future = publish_func(topic_path, data=data, index=str(i))
            callback(future)

    # Publish messages.
    publish_messages(publisher.publish, callback=resolve_future_callback)
    print('\nPublished all messages.')

    def process_message_callback(message):
        message.ack()
        subtime = time.time()
        tracker[message.message_id]['subtime'] = subtime
        print(message.attributes['index'])

    # Receive messages asynchronously.
    subscriber.subscribe(subscription_path, callback=process_message_callback)
    print('\nListening for messages...')

    while True:
        # Extract delivery times from `tracker` and deplete it over time.
        for message_id in list(tracker):
            if tracker[message_id]['subtime'] is not None:
                delivery_times.append(tracker[message_id]['subtime'] -
                                      tracker[message_id]['pubtime'])
                del tracker[message_id]

        # Exit if all the delivery times have been accounted for.
        if len(tracker) == 0:
            print('\nDelivery Statistics')
            print('Average time: {:.6f}s'.format(
                sum(delivery_times)/len(delivery_times)))
            print('Best time: {:.6f}s'.format(min(delivery_times)))
            break
        else:
            # Sleep the thread at 5Hz to save on resources.
            time.sleep(1./5)
    # [END pubsub_end_to_end]
    return delivery_times


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

    standard_parser = subparsers.add_parser('standard',
                                            help=end_to_end_standard.__doc__)
    standard_parser.add_argument('topic_name', help='Your topic name')
    standard_parser.add_argument('subscription_name',
                                 help='Your subscription name')

    args = parser.parse_args()

    if args.command == 'basic':
        end_to_end(args.project_id, args.topic_name, args.subscription_name)
