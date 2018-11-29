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
    # [START pubsub_quickstart_end2end_basic]
    import time

    from google.api_core.exceptions import NotFound
    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"
    # TODO subscription_name = "Your Pub/Sub subscription name"
    # TODO num_messages = number of messages to test end-to-end

    # Instantiate a publisher and a subscriber client
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_name}`
    topic_path = publisher.topic_path(project_id, topic_name)

    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_name}`
    subscription_path = subscriber.subscription_path(
        project_id, subscription_name)

    # Create a topic.
    try:
        publisher.delete_topic(topic_path)
    except NotFound:
        pass
    finally:
        topic = publisher.create_topic(topic_path)
        print('Topic created: \"{}\"'.format(topic.name))

    # Create a subscription.
    try:
        subscriber.delete_subscription(subscription_path)
    except NotFound:
        pass
    finally:
        subscription = subscriber.create_subscription(
            subscription_path, topic_path)
        print('Subscription created: \"{}\"'.format(subscription.name))

    # `data` is roughly 10 Kb.
    data = 'x' * 9600
    # `data` must be a bytestring.
    data = data.encode('utf-8')
    # Initialize an empty dictionary to track messages.
    tracker = dict()
    pubsub_time = 0.0

    # Publish messages.
    for i in range(num_messages):
        # When we publish a message, the client returns a future.
        future = publisher.publish(topic_path, data=data)

        tracker.update({i: {'index': i,
                            'pubtime': time.time(),
                            'subtime': None}})

        # `future.result()` blocks and returns a unique message ID per message.
        tracker[future.result()] = tracker.pop(i)

    print('\nPublished all messages.')

    def callback(message):
        # Unacknowledged messages will be sent again.
        message.ack()
        # Update message `subtime`.
        tracker[message.message_id]['subtime'] = time.time()

    # Receive messages. The subscriber is nonblocking.
    subscriber.subscribe(subscription_path, callback=callback)

    print('\nListening for messages...')

    while True:
        # Deplete messages in `tracker` every time we have complete info
        # of a message.
        for msg_id in list(tracker):
            pubtime = tracker[msg_id]['pubtime']
            subtime = tracker[msg_id]['subtime']
            if subtime is not None:
                pubsub_time += subtime - pubtime
                del tracker[msg_id]

        # Exit if `tracker` is empty i.e. all the messages' publish-subscribe
        # time have been accounted for.
        if len(tracker) == 0:
            print('\nTotal publish to subscribe time for {} messages: \
                  {:.6f}s.'.format(num_messages, pubsub_time))
            break
        else:
            print('Messages countdown: {}'.format(len(tracker)))
            # Sleep the thread at 5Hz to save on resources.
            time.sleep(1./5)
    # [END pubsub_quickstart_end2end_basic]


def end_to_end_standard(project_id, topic_name, subscription_name,
                        num_messages):
    # [START pubsub_quickstart_end2end_standard]
    pass
    # [END pubsub_quickstart_end2end_standard]


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
    basic_parser.add_argument('num_messages', type=int,
                              help='Number of test messages')

    standard_parser = subparsers.add_parser('standard',
                                            help=end_to_end_standard.__doc__)
    standard_parser.add_argument('topic_name', help='Your topic name')
    standard_parser.add_argument('subscription_name',
                                 help='Your subscription name')
    standard_parser.add_argument('num_messages', type=int,
                                 help='Number of test messages')

    args = parser.parse_args()

    if args.command == 'basic':
        end_to_end(args.project_id, args.topic_name, args.subscription_name,
                   args.num_messages)
    if args.command == 'standard':
        end_to_end_standard(args.project_id, args.topic_name,
                            args.subscription_name, args.num_messages)
