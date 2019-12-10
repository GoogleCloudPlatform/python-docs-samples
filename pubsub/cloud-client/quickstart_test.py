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

import os
import uuid

from google.cloud import pubsub_v1
import pytest
import quickstart

UUID = uuid.uuid4().hex
PROJECT = os.environ["GCLOUD_PROJECT"]
TOPIC = "end-to-end-test-topic-" + UUID
SUBSCRIPTION = "end-to-end-test-topic-sub-" + UUID
N = 10


@pytest.fixture(scope="module")
def publisher_client():
    yield pubsub_v1.PublisherClient()


@pytest.fixture(scope="module")
def topic(publisher_client):
    topic_path = publisher_client.topic_path(PROJECT, TOPIC)

    try:
        publisher_client.delete_topic(topic_path)
    except Exception:
        pass

    yield TOPIC

    publisher_client.delete_topic(topic_path)


@pytest.fixture(scope="module")
def subscriber_client():
    yield pubsub_v1.SubscriberClient()


@pytest.fixture(scope="module")
def subscription(subscriber_client, topic):
    subscription_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION
    )

    try:
        subscriber_client.delete_subscription(subscription_path)
    except Exception:
        pass

    yield SUBSCRIPTION

    subscriber_client.delete_subscription(subscription_path)


def test_end_to_end(topic, subscription, capsys):

    quickstart.end_to_end(PROJECT, topic, subscription, N)
    out, _ = capsys.readouterr()

    assert "Received all messages" in out
    assert "Publish time lapsed" in out
    assert "Subscribe time lapsed" in out
