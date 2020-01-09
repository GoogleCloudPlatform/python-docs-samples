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


import argparse


def end_to_end(project_id, topic_name, subscription_name, num_messages):
    # [START pubsub_end_to_end]
    import time

    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"
    # TODO num_messages = number of messages to test end-to-end

    # Instantiates a publisher and subscriber client
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_name}`
    topic_path = subscriber.topic_path(project_id, topic_name)

    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_name}`
    subscription_path = subscriber.subscription_path(
        project_id, subscription_name
    )

    # Create the topic.
    topic = publisher.create_topic(topic_path)
    print("\nTopic created: {}".format(topic.name))

    # Create a subscription.
    subscription = subscriber.create_subscription(
        subscription_path, topic_path
    )
    print("\nSubscription created: {}\n".format(subscription.name))

    publish_begin = time.time()

    # Publish messages.
    for n in range(num_messages):
        data = u"Message number {}".format(n)
        # Data must be a bytestring
        data = data.encode("utf-8")
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, data=data)
        print("Published {} of message ID {}.".format(data, future.result()))

    publish_time = time.time() - publish_begin

    messages = set()

    def callback(message):
        print("Received message: {}".format(message))
        # Unacknowledged messages will be sent again.
        message.ack()
        messages.add(message)

    subscribe_begin = time.time()

    # Receive messages. The subscriber is nonblocking.
    subscriber.subscribe(subscription_path, callback=callback)

    print("\nListening for messages on {}...\n".format(subscription_path))

    while True:
        if len(messages) == num_messages:
            subscribe_time = time.time() - subscribe_begin
            print("\nReceived all messages.")
            print("Publish time lapsed: {:.2f}s.".format(publish_time))
            print("Subscribe time lapsed: {:.2f}s.".format(subscribe_time))
            break
        else:
            # Sleeps the thread at 50Hz to save on resources.
            time.sleep(1.0 / 50)
    # [END pubsub_end_to_end]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID")
    parser.add_argument("topic_name", help="Your topic name")
    parser.add_argument("subscription_name", help="Your subscription name")
    parser.add_argument("num_msgs", type=int, help="Number of test messages")

    args = parser.parse_args()

    end_to_end(
        args.project_id, args.topic_name, args.subscription_name, args.num_msgs
    )
