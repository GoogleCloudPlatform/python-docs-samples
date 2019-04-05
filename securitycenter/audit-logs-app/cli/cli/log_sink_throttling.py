#!/usr/bin/env python3

import sys
import click
from time import sleep
from google.cloud import pubsub_v1

@click.command()
@click.option('--project', help='Project ID.', required=True)
@click.option('--subscription', help='Pub/Sub subscription name.', required=True)
@click.option('--forward-topic', help='Pub/Sub forward topic name.', required=True)
@click.option('--sleep-seconds', help='Seconds to sleep between forwarding each message.', default=2)
@click.option('--print-messages/--no-print-messages', help='Print message data.', default=False)
              
def forward(project, subscription, forward_topic, sleep_seconds, print_messages):
    print("Using project: {}".format(project))
    print("Creating the subscriber: {}".format(subscription))
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription)

    print("Creating the publisher: {}".format(forward_topic))
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, forward_topic)

    print("Pulling messages...")
    while True:
        ack_ids = []
        try:
            response = subscriber.pull(
                subscription_path,
                max_messages=10,
                return_immediately=False)

            print("Forwarding {} messages...".format(len(response.received_messages)))
            for received_message in response.received_messages:
                if print_messages:
                    print("Message received: {}".format(received_message.message.data))
                publisher.publish(topic_path, data=received_message.message.data)
                ack_ids.append(received_message.ack_id)
                print("Message with ID {} forwarded to topic {}. Sleeping for {} seconds." \
                    .format(received_message.message.message_id, forward_topic, sleep_seconds))
                sleep(sleep_seconds)

            ack_messages(subscriber, subscription_path, ack_ids)
            print("Pulling more messages...")
        except (KeyboardInterrupt, KeyError):
            sys.exit()
        except Exception as e:
            # an error occured, log the error and try to ack anyway...
            try:
                print("An error occured! {}".format(e))
                ack_messages(subscriber, subscription_path, ack_ids)
            except:
                print("Error trying to ack the messages.")
            finally:
                print("Continuing to pull more messages...")


def ack_messages(subscriber, subscription_path, ack_ids):
    subscriber.acknowledge(subscription_path, ack_ids)
    print("{} messages acknowledged.".format(len(ack_ids)))

if __name__ == '__main__':
    forward()
