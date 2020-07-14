#!/usr/bin/env python
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Demo for receiving notifications."""


def receive_notifications(project_id, subscription_name):
    # [START scc_receive_notifications]
    # Requires https://cloud.google.com/pubsub/docs/quickstart-client-libraries#pubsub-client-libraries-python
    import concurrent

    from google.cloud import pubsub_v1
    from google.cloud.securitycenter_v1.proto.notification_message_pb2 import (
        NotificationMessage,
    )
    from google.protobuf import json_format

    # TODO: project_id = "your-project-id"
    # TODO: subscription_name = "your-subscription-name"

    def callback(message):
        print("Received message")

        notification_msg = NotificationMessage()
        json_format.Parse(message.data, notification_msg)

        print(
            "Notification config name: {}".format(
                notification_msg.notification_config_name
            )
        )
        print("Finding: {}".format(notification_msg.finding))

        # Ack the message to prevent it from being pulled again
        message.ack()

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    print("Listening for messages on {}...\n".format(subscription_path))
    try:
        streaming_pull_future.result(timeout=1)  # Block for 1 second
    except concurrent.futures.TimeoutError:
        streaming_pull_future.cancel()
    # [END scc_receive_notifications]
    return True
