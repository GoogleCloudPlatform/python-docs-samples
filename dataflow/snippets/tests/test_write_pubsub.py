# !/usr/bin/env python
#  Copyright 2024 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import time
from unittest.mock import patch
import uuid

from google.cloud import pubsub_v1

import pytest

from ..write_pubsub import write_to_pubsub


topic_id = f"test-topic-{uuid.uuid4()}"
subscription_id = f"{topic_id}-sub"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

NUM_MESSAGES = 4
TIMEOUT = 60 * 5


@pytest.fixture(scope="function")
def setup_and_teardown() -> None:
    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    try:
        publisher.create_topic(request={"name": topic_path})
        subscriber.create_subscription(
            request={"name": subscription_path, "topic": topic_path}
        )
        yield
    finally:
        subscriber.delete_subscription(request={"subscription": subscription_path})
        publisher.delete_topic(request={"topic": topic_path})


def read_messages() -> None:
    received_messages = []
    ack_ids = []

    # Read messages from Pub/Sub. It might be necessary to read multiple
    # batches, Use a timeout value to avoid potentially looping forever.
    start_time = time.time()
    while time.time() - start_time <= TIMEOUT:
        # Pull messages from Pub/Sub.
        subscription_path = subscriber.subscription_path(project_id, subscription_id)
        response = subscriber.pull(
            request={"subscription": subscription_path, "max_messages": NUM_MESSAGES}
        )
        received_messages.append(response.received_messages)

        for received_message in response.received_messages:
            ack_ids.append(received_message.ack_id)

        # Acknowledge the received messages so they will not be sent again.
        subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": ack_ids}
        )

        if len(received_messages) >= NUM_MESSAGES:
            break

        time.sleep(5)

    return received_messages


def test_write_to_pubsub(setup_and_teardown: None) -> None:
    topic_path = publisher.topic_path(project_id, topic_id)
    with patch("sys.argv", ["", "--streaming", f"--topic={topic_path}"]):
        write_to_pubsub()

        # Read from Pub/Sub to verify the pipeline successfully wrote messages.
        # Duplicate reads are possible.
        messages = read_messages()
        assert len(messages) >= NUM_MESSAGES
