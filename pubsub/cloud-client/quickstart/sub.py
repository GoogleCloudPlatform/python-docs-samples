#!/usr/bin/env python

# Copyright 2019 Google LLC
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

# [START pubsub_quickstart_sub_all]
import argparse

# [START pubsub_quickstart_sub_deps]
from google.cloud import pubsub_v1

# [END pubsub_quickstart_sub_deps]


def sub(project_id, subscription_name):
    """Receives messages from a Pub/Sub subscription."""
    # [START pubsub_quickstart_sub_client]
    # Initialize a Subscriber client
    client = pubsub_v1.SubscriberClient()
    # [END pubsub_quickstart_sub_client]
    # Create a fully qualified identifier in the form of
    # `projects/{project_id}/subscriptions/{subscription_name}`
    subscription_path = client.subscription_path(project_id, subscription_name)

    def callback(message):
        print(
            "Received message {} of message ID {}\n".format(
                message, message.message_id
            )
        )
        # Acknowledge the message. Unack'ed messages will be redelivered.
        message.ack()
        print("Acknowledged message {}\n".format(message.message_id))

    streaming_pull_future = client.subscribe(
        subscription_path, callback=callback
    )
    print("Listening for messages on {}..\n".format(subscription_path))

    # Calling result() on StreamingPullFuture keeps the main thread from
    # exiting while messages get processed in the callbacks.
    try:
        streaming_pull_future.result()
    except:  # noqa
        streaming_pull_future.cancel()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Google Cloud project ID")
    parser.add_argument("subscription_name", help="Pub/Sub subscription name")

    args = parser.parse_args()

    sub(args.project_id, args.subscription_name)
# [END pubsub_quickstart_sub_all]
