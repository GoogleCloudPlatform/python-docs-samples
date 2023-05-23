#!/bin/python
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START containeranalysis_pubsub]
import time

from google.api_core.exceptions import AlreadyExists
from google.cloud.pubsub import SubscriberClient
from google.cloud.pubsub_v1.subscriber.message import Message


def pubsub(subscription_id: str, timeout_seconds: int, project_id: str) -> int:
    """Respond to incoming occurrences using a Cloud Pub/Sub subscription."""
    # subscription_id := 'my-occurrences-subscription'
    # timeout_seconds = 20
    # project_id = 'my-gcp-project'

    client = SubscriberClient()
    subscription_name = client.subscription_path(project_id, subscription_id)
    receiver = MessageReceiver()
    client.subscribe(subscription_name, receiver.pubsub_callback)

    # listen for 'timeout' seconds
    for _ in range(timeout_seconds):
        time.sleep(1)
    # print and return the number of pubsub messages received
    print(receiver.msg_count)
    return receiver.msg_count


class MessageReceiver:
    """Custom class to handle incoming Pub/Sub messages."""

    def __init__(self) -> None:
        # initialize counter to 0 on initialization
        self.msg_count = 0

    def pubsub_callback(self, message: Message) -> None:
        # every time a pubsub message comes in, print it and count it
        self.msg_count += 1
        print(f"Message {self.msg_count}: {message.data}")
        message.ack()


def create_occurrence_subscription(subscription_id: str, project_id: str) -> bool:
    """Creates a new Pub/Sub subscription object listening to the
    Container Analysis Occurrences topic."""
    # subscription_id := 'my-occurrences-subscription'
    # project_id = 'my-gcp-project'

    topic_id = "container-analysis-occurrences-v1"
    client = SubscriberClient()
    topic_name = f"projects/{project_id}/topics/{topic_id}"
    subscription_name = client.subscription_path(project_id, subscription_id)
    success = True
    try:
        client.create_subscription({"name": subscription_name, "topic": topic_name})
    except AlreadyExists:
        # if subscription already exists, do nothing
        pass
    else:
        success = False
    return success


# [END containeranalysis_pubsub]
