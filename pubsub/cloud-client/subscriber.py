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

"""This application demonstrates how to perform basic operations on
subscriptions with the Cloud Pub/Sub API.

For more information, see the README.md under /pubsub and the documentation
at https://cloud.google.com/pubsub/docs.
"""

import argparse


def list_subscriptions_in_topic(project_id, topic_name):
    """Lists all subscriptions for a given topic."""
    # [START pubsub_list_topic_subscriptions]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_name = "your-topic-id"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    for subscription in publisher.list_topic_subscriptions(topic_path):
        print(subscription)
    # [END pubsub_list_topic_subscriptions]


def list_subscriptions_in_project(project_id):
    """Lists all subscriptions in the current project."""
    # [START pubsub_list_subscriptions]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"

    subscriber = pubsub_v1.SubscriberClient()
    project_path = subscriber.project_path(project_id)

    for subscription in subscriber.list_subscriptions(project_path):
        print(subscription.name)

    subscriber.close()
    # [END pubsub_list_subscriptions]


def create_subscription(project_id, topic_name, subscription_name):
    """Create a new pull subscription on the given topic."""
    # [START pubsub_create_pull_subscription]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_name = "your-topic-id"
    # subscription_name = "your-subscription-id"

    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    subscription = subscriber.create_subscription(subscription_path, topic_path)

    print("Subscription created: {}".format(subscription))

    subscriber.close()
    # [END pubsub_create_pull_subscription]


def create_subscription_with_dead_letter_topic(
    project_id, topic_name, subscription_name, dead_letter_topic_name
):
    """Create a subscription with dead letter policy."""
    # [START pubsub_dead_letter_create_subscription]
    from google.cloud import pubsub_v1
    from google.cloud.pubsub_v1.types import DeadLetterPolicy

    # TODO(developer)
    # project_id = "your-project-id"
    # endpoint = "https://my-test-project.appspot.com/push"
    # TODO(developer): This is an existing topic that the subscription
    # with dead letter policy is attached to.
    # topic_name = "your-topic-id"
    # TODO(developer): This is an existing subscription with a dead letter policy.
    # subscription_name = "your-subscription-id"
    # TODO(developer): This is an existing dead letter topic that the subscription
    # with dead letter policy will forward dead letter messages to.
    # dead_letter_topic_name = "your-dead-letter-topic-id"

    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    dead_letter_topic_path = subscriber.topic_path(project_id, dead_letter_topic_name)

    dead_letter_policy = DeadLetterPolicy(
        dead_letter_topic=dead_letter_topic_path, max_delivery_attempts=10
    )

    with subscriber:
        subscription = subscriber.create_subscription(
            subscription_path, topic_path, dead_letter_policy=dead_letter_policy
        )

    print("Subscription created: {}".format(subscription.name))
    print(
        "It will forward dead letter messages to: {}".format(
            subscription.dead_letter_policy.dead_letter_topic
        )
    )
    print(
        "After {} delivery attempts.".format(
            subscription.dead_letter_policy.max_delivery_attempts
        )
    )
    # [END pubsub_dead_letter_create_subscription]


def create_push_subscription(project_id, topic_name, subscription_name, endpoint):
    """Create a new push subscription on the given topic."""
    # [START pubsub_create_push_subscription]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_name = "your-topic-id"
    # subscription_name = "your-subscription-id"
    # endpoint = "https://my-test-project.appspot.com/push"

    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    push_config = pubsub_v1.types.PushConfig(push_endpoint=endpoint)

    subscription = subscriber.create_subscription(
        subscription_path, topic_path, push_config
    )

    print("Push subscription created: {}".format(subscription))
    print("Endpoint for subscription is: {}".format(endpoint))

    subscriber.close()
    # [END pubsub_create_push_subscription]


def delete_subscription(project_id, subscription_name):
    """Deletes an existing Pub/Sub topic."""
    # [START pubsub_delete_subscription]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_name = "your-subscription-id"

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    subscriber.delete_subscription(subscription_path)

    print("Subscription deleted: {}".format(subscription_path))

    subscriber.close()
    # [END pubsub_delete_subscription]


def update_push_subscription(project_id, topic_name, subscription_name, endpoint):
    """
    Updates an existing Pub/Sub subscription's push endpoint URL.
    Note that certain properties of a subscription, such as
    its topic, are not modifiable.
    """
    # [START pubsub_update_push_configuration]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_name = "your-topic-id"
    # subscription_name = "your-subscription-id"
    # endpoint = "https://my-test-project.appspot.com/push"

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    push_config = pubsub_v1.types.PushConfig(push_endpoint=endpoint)

    subscription = pubsub_v1.types.Subscription(
        name=subscription_path, topic=topic_name, push_config=push_config
    )

    update_mask = {"paths": {"push_config"}}

    result = subscriber.update_subscription(subscription, update_mask)

    print("Subscription updated: {}".format(subscription_path))
    print("New endpoint for subscription is: {}".format(result.push_config))

    subscriber.close()
    # [END pubsub_update_push_configuration]


def update_subscription_with_dead_letter_policy(
    project_id, topic_name, subscription_name, dead_letter_topic_name
):
    """Update a subscription's dead letter policy."""
    # [START pubsub_dead_letter_update_subscription]
    from google.cloud import pubsub_v1
    from google.cloud.pubsub_v1.types import DeadLetterPolicy, FieldMask

    # TODO(developer)
    # project_id = "your-project-id"
    # TODO(developer): This is an existing topic that the subscription
    # with dead letter policy is attached to.
    # topic_name = "your-topic-name"
    # TODO(developer): This is an existing subscription with a dead letter policy.
    # subscription_name = "your-subscription-id"
    # TODO(developer): This is an existing dead letter topic that the subscription
    # with dead letter policy will forward dead letter messages to.
    # dead_letter_topic_name = "your-dead-letter-topic-id"

    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    dead_letter_topic_path = subscriber.topic_path(project_id, dead_letter_topic_name)

    subscription_before_update = subscriber.get_subscription(subscription_path)
    print("Before the update: {}".format(subscription_before_update))

    # Indicates which fields in the provided subscription to update.
    update_mask = FieldMask(paths=["dead_letter_policy.max_delivery_attempts"])

    # Construct a dead letter policy you expect to have after the update.
    dead_letter_policy = DeadLetterPolicy(
        dead_letter_topic=dead_letter_topic_path, max_delivery_attempts=20
    )

    # Construct the subscription with the dead letter policy you expect to have
    # after the update. Here, values in the required fields (name, topic) help
    # identify the subscription.
    subscription = pubsub_v1.types.Subscription(
        name=subscription_path, topic=topic_path, dead_letter_policy=dead_letter_policy,
    )

    with subscriber:
        subscription_after_update = subscriber.update_subscription(
            subscription, update_mask
        )

    print("After the update: {}".format(subscription_after_update))
    # [END pubsub_dead_letter_update_subscription]
    return subscription_after_update


def remove_dead_letter_policy(project_id, topic_name, subscription_name):
    """Remove dead letter policy from a subscription."""
    # [START pubsub_dead_letter_remove]
    from google.cloud import pubsub_v1
    from google.cloud.pubsub_v1.types import FieldMask

    # TODO(developer)
    # project_id = "your-project-id"
    # TODO(developer): This is an existing topic that the subscription
    # with dead letter policy is attached to.
    # topic_name = "your-topic-name"
    # TODO(developer): This is an existing subscription with a dead letter policy.
    # subscription_name = "your-subscription-id"

    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    subscription_before_update = subscriber.get_subscription(subscription_path)
    print("Before removing the policy: {}".format(subscription_before_update))

    # Indicates which fields in the provided subscription to update.
    update_mask = FieldMask(
        paths=[
            "dead_letter_policy.dead_letter_topic",
            "dead_letter_policy.max_delivery_attempts",
        ]
    )

    # Construct the subscription (without any dead letter policy) that you
    # expect to have after the update.
    subscription = pubsub_v1.types.Subscription(
        name=subscription_path, topic=topic_path
    )

    with subscriber:
        subscription_after_update = subscriber.update_subscription(
            subscription, update_mask
        )

    print("After removing the policy: {}".format(subscription_after_update))
    # [END pubsub_dead_letter_remove]
    return subscription_after_update


def receive_messages(project_id, subscription_name, timeout=None):
    """Receives messages from a pull subscription."""
    # [START pubsub_subscriber_async_pull]
    # [START pubsub_quickstart_subscriber]
    from concurrent.futures import TimeoutError
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_name = "your-subscription-id"
    # Number of seconds the subscriber should listen for messages
    # timeout = 5.0

    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_name}`
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback(message):
        print("Received message: {}".format(message))
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print("Listening for messages on {}..\n".format(subscription_path))

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
    # [END pubsub_subscriber_async_pull]
    # [END pubsub_quickstart_subscriber]


def receive_messages_with_custom_attributes(
    project_id, subscription_name, timeout=None
):
    """Receives messages from a pull subscription."""
    # [START pubsub_subscriber_sync_pull_custom_attributes]
    # [START pubsub_subscriber_async_pull_custom_attributes]
    from concurrent.futures import TimeoutError
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_name = "your-subscription-id"
    # Number of seconds the subscriber should listen for messages
    # timeout = 5.0

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback(message):
        print("Received message: {}".format(message.data))
        if message.attributes:
            print("Attributes:")
            for key in message.attributes:
                value = message.attributes.get(key)
                print("{}: {}".format(key, value))
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print("Listening for messages on {}..\n".format(subscription_path))

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
    # [END pubsub_subscriber_async_pull_custom_attributes]
    # [END pubsub_subscriber_sync_pull_custom_attributes]


def receive_messages_with_flow_control(project_id, subscription_name, timeout=None):
    """Receives messages from a pull subscription with flow control."""
    # [START pubsub_subscriber_flow_settings]
    from concurrent.futures import TimeoutError
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_name = "your-subscription-id"
    # Number of seconds the subscriber should listen for messages
    # timeout = 5.0

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback(message):
        print("Received message: {}".format(message.data))
        message.ack()

    # Limit the subscriber to only have ten outstanding messages at a time.
    flow_control = pubsub_v1.types.FlowControl(max_messages=10)

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback, flow_control=flow_control
    )
    print("Listening for messages on {}..\n".format(subscription_path))

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
    # [END pubsub_subscriber_flow_settings]


def synchronous_pull(project_id, subscription_name):
    """Pulling messages synchronously."""
    # [START pubsub_subscriber_sync_pull]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_name = "your-subscription-id"

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    NUM_MESSAGES = 3

    # The subscriber pulls a specific number of messages.
    response = subscriber.pull(subscription_path, max_messages=NUM_MESSAGES)

    ack_ids = []
    for received_message in response.received_messages:
        print("Received: {}".format(received_message.message.data))
        ack_ids.append(received_message.ack_id)

    # Acknowledges the received messages so they will not be sent again.
    subscriber.acknowledge(subscription_path, ack_ids)

    print(
        "Received and acknowledged {} messages. Done.".format(
            len(response.received_messages)
        )
    )

    subscriber.close()
    # [END pubsub_subscriber_sync_pull]


def synchronous_pull_with_lease_management(project_id, subscription_name):
    """Pulling messages synchronously with lease management"""
    # [START pubsub_subscriber_sync_pull_with_lease]
    import logging
    import multiprocessing
    import random
    import time

    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_name = "your-subscription-id"

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    NUM_MESSAGES = 2
    ACK_DEADLINE = 30
    SLEEP_TIME = 10

    # The subscriber pulls a specific number of messages.
    response = subscriber.pull(subscription_path, max_messages=NUM_MESSAGES)

    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)

    def worker(msg):
        """Simulates a long-running process."""
        RUN_TIME = random.randint(1, 60)
        logger.info(
            "{}: Running {} for {}s".format(
                time.strftime("%X", time.gmtime()), msg.message.data, RUN_TIME
            )
        )
        time.sleep(RUN_TIME)

    # `processes` stores process as key and ack id and message as values.
    processes = dict()
    for message in response.received_messages:
        process = multiprocessing.Process(target=worker, args=(message,))
        processes[process] = (message.ack_id, message.message.data)
        process.start()

    while processes:
        for process in list(processes):
            ack_id, msg_data = processes[process]
            # If the process is still running, reset the ack deadline as
            # specified by ACK_DEADLINE once every while as specified
            # by SLEEP_TIME.
            if process.is_alive():
                # `ack_deadline_seconds` must be between 10 to 600.
                subscriber.modify_ack_deadline(
                    subscription_path, [ack_id], ack_deadline_seconds=ACK_DEADLINE,
                )
                logger.info(
                    "{}: Reset ack deadline for {} for {}s".format(
                        time.strftime("%X", time.gmtime()), msg_data, ACK_DEADLINE,
                    )
                )

            # If the processs is finished, acknowledges using `ack_id`.
            else:
                subscriber.acknowledge(subscription_path, [ack_id])
                logger.info(
                    "{}: Acknowledged {}".format(
                        time.strftime("%X", time.gmtime()), msg_data
                    )
                )
                processes.pop(process)

        # If there are still processes running, sleeps the thread.
        if processes:
            time.sleep(SLEEP_TIME)

    print(
        "Received and acknowledged {} messages. Done.".format(
            len(response.received_messages)
        )
    )

    subscriber.close()
    # [END pubsub_subscriber_sync_pull_with_lease]


def listen_for_errors(project_id, subscription_name, timeout=None):
    """Receives messages and catches errors from a pull subscription."""
    # [START pubsub_subscriber_error_listener]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "Your Google Cloud Project ID"
    # subscription_name = "Your Pubsub subscription name"
    # Number of seconds the subscriber should listen for messages
    # timeout = 5.0

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback(message):
        print("Received message: {}".format(message))
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print("Listening for messages on {}..\n".format(subscription_path))

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        try:
            streaming_pull_future.result(timeout=timeout)
        except Exception as e:
            streaming_pull_future.cancel()
            print(
                "Listening for messages on {} threw an exception: {}.".format(
                    subscription_name, e
                )
            )
    # [END pubsub_subscriber_error_listener]


def receive_messages_with_delivery_attempts(
    project_id, subscription_name, timeout=None
):
    # [START  pubsub_dead_letter_delivery_attempt]
    from concurrent.futures import TimeoutError
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_name = "your-subscription-id"

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback(message):
        print("Received message: {}".format(message))
        print("With delivery attempts: {}".format(message.delivery_attempt))
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print("Listening for messages on {}..\n".format(subscription_path))

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
    # [END  pubsub_dead_letter_delivery_attempt]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID")

    subparsers = parser.add_subparsers(dest="command")
    list_in_topic_parser = subparsers.add_parser(
        "list-in-topic", help=list_subscriptions_in_topic.__doc__
    )
    list_in_topic_parser.add_argument("topic_name")

    list_in_project_parser = subparsers.add_parser(
        "list-in-project", help=list_subscriptions_in_project.__doc__
    )

    create_parser = subparsers.add_parser("create", help=create_subscription.__doc__)
    create_parser.add_argument("topic_name")
    create_parser.add_argument("subscription_name")

    create_with_dead_letter_policy_parser = subparsers.add_parser(
        "create-with-dead-letter-policy",
        help=create_subscription_with_dead_letter_topic.__doc__,
    )
    create_with_dead_letter_policy_parser.add_argument("topic_name")
    create_with_dead_letter_policy_parser.add_argument("subscription_name")
    create_with_dead_letter_policy_parser.add_argument("dead_letter_topic_name")

    create_push_parser = subparsers.add_parser(
        "create-push", help=create_push_subscription.__doc__
    )
    create_push_parser.add_argument("topic_name")
    create_push_parser.add_argument("subscription_name")
    create_push_parser.add_argument("endpoint")

    delete_parser = subparsers.add_parser("delete", help=delete_subscription.__doc__)
    delete_parser.add_argument("subscription_name")

    update_push_parser = subparsers.add_parser(
        "update-push", help=update_push_subscription.__doc__
    )
    update_push_parser.add_argument("topic_name")
    update_push_parser.add_argument("subscription_name")
    update_push_parser.add_argument("endpoint")

    update_dead_letter_policy_parser = subparsers.add_parser(
        "update-dead-letter-policy",
        help=update_subscription_with_dead_letter_policy.__doc__,
    )
    update_dead_letter_policy_parser.add_argument("topic_name")
    update_dead_letter_policy_parser.add_argument("subscription_name")
    update_dead_letter_policy_parser.add_argument("dead_letter_topic_name")

    remove_dead_letter_policy_parser = subparsers.add_parser(
        "remove-dead-letter-policy", help=remove_dead_letter_policy.__doc__
    )
    remove_dead_letter_policy_parser.add_argument("topic_name")
    remove_dead_letter_policy_parser.add_argument("subscription_name")

    receive_parser = subparsers.add_parser("receive", help=receive_messages.__doc__)
    receive_parser.add_argument("subscription_name")
    receive_parser.add_argument("--timeout", default=None, type=float)

    receive_with_custom_attributes_parser = subparsers.add_parser(
        "receive-custom-attributes",
        help=receive_messages_with_custom_attributes.__doc__,
    )
    receive_with_custom_attributes_parser.add_argument("subscription_name")
    receive_with_custom_attributes_parser.add_argument(
        "--timeout", default=None, type=float
    )

    receive_with_flow_control_parser = subparsers.add_parser(
        "receive-flow-control", help=receive_messages_with_flow_control.__doc__
    )
    receive_with_flow_control_parser.add_argument("subscription_name")
    receive_with_flow_control_parser.add_argument("--timeout", default=None, type=float)

    synchronous_pull_parser = subparsers.add_parser(
        "receive-synchronously", help=synchronous_pull.__doc__
    )
    synchronous_pull_parser.add_argument("subscription_name")

    synchronous_pull_with_lease_management_parser = subparsers.add_parser(
        "receive-synchronously-with-lease",
        help=synchronous_pull_with_lease_management.__doc__,
    )
    synchronous_pull_with_lease_management_parser.add_argument("subscription_name")

    listen_for_errors_parser = subparsers.add_parser(
        "listen-for-errors", help=listen_for_errors.__doc__
    )
    listen_for_errors_parser.add_argument("subscription_name")
    listen_for_errors_parser.add_argument("--timeout", default=None, type=float)

    receive_messages_with_delivery_attempts_parser = subparsers.add_parser(
        "receive-messages-with-delivery-attempts",
        help=receive_messages_with_delivery_attempts.__doc__,
    )
    receive_messages_with_delivery_attempts_parser.add_argument("subscription_name")
    receive_messages_with_delivery_attempts_parser.add_argument(
        "--timeout", default=None, type=float
    )

    args = parser.parse_args()

    if args.command == "list-in-topic":
        list_subscriptions_in_topic(args.project_id, args.topic_name)
    elif args.command == "list-in-project":
        list_subscriptions_in_project(args.project_id)
    elif args.command == "create":
        create_subscription(args.project_id, args.topic_name, args.subscription_name)
    elif args.command == "create-with-dead-letter-policy":
        create_subscription_with_dead_letter_topic(
            args.project_id,
            args.topic_name,
            args.subscription_name,
            args.dead_letter_topic_name,
        )
    elif args.command == "create-push":
        create_push_subscription(
            args.project_id, args.topic_name, args.subscription_name, args.endpoint,
        )
    elif args.command == "delete":
        delete_subscription(args.project_id, args.subscription_name)
    elif args.command == "update-push":
        update_push_subscription(
            args.project_id, args.topic_name, args.subscription_name, args.endpoint,
        )
    elif args.command == "update-dead-letter-policy":
        update_subscription_with_dead_letter_policy(
            args.project_id,
            args.topic_name,
            args.subscription_name,
            args.dead_letter_topic_name,
        )
    elif args.command == "remove-dead-letter-policy":
        remove_dead_letter_policy(
            args.project_id, args.topic_name, args.subscription_name
        )
    elif args.command == "receive":
        receive_messages(args.project_id, args.subscription_name, args.timeout)
    elif args.command == "receive-custom-attributes":
        receive_messages_with_custom_attributes(
            args.project_id, args.subscription_name, args.timeout
        )
    elif args.command == "receive-flow-control":
        receive_messages_with_flow_control(
            args.project_id, args.subscription_name, args.timeout
        )
    elif args.command == "receive-synchronously":
        synchronous_pull(args.project_id, args.subscription_name)
    elif args.command == "receive-synchronously-with-lease":
        synchronous_pull_with_lease_management(args.project_id, args.subscription_name)
    elif args.command == "listen-for-errors":
        listen_for_errors(args.project_id, args.subscription_name, args.timeout)
    elif args.command == "receive-messages-with-delivery-attempts":
        receive_messages_with_delivery_attempts(
            args.project_id, args.subscription_name, args.timeout
        )
