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

import mock
import os
import pytest
import uuid

from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1

import sub


UUID = uuid.uuid4().hex
PROJECT = os.environ["GCLOUD_PROJECT"]
TOPIC = "quickstart-sub-test-topic-" + UUID
SUBSCRIPTION = "quickstart-sub-test-topic-sub-" + UUID

publisher_client = pubsub_v1.PublisherClient()
subscriber_client = pubsub_v1.SubscriberClient()


@pytest.fixture(scope="module")
def topic_path():
    topic_path = publisher_client.topic_path(PROJECT, TOPIC)

    try:
        topic = publisher_client.create_topic(topic_path)
        yield topic.name
    except AlreadyExists:
        yield topic_path

    publisher_client.delete_topic(topic_path)


@pytest.fixture(scope="module")
def subscription_path(topic_path):
    subscription_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION
    )

    try:
        subscription = subscriber_client.create_subscription(
            subscription_path, topic_path
        )
        yield subscription.name
    except AlreadyExists:
        yield subscription_path

    subscriber_client.delete_subscription(subscription_path)


def _publish_messages(topic_path):
    publish_future = publisher_client.publish(topic_path, data=b"Hello World!")
    publish_future.result()


def test_sub(monkeypatch, topic_path, subscription_path, capsys):

    real_client = pubsub_v1.SubscriberClient()
    mock_client = mock.Mock(spec=pubsub_v1.SubscriberClient, wraps=real_client)

    # Attributes on mock_client_constructor uses the corresponding
    # attributes on pubsub_v1.SubscriberClient.
    mock_client_constructor = mock.create_autospec(pubsub_v1.SubscriberClient)
    mock_client_constructor.return_value = mock_client

    monkeypatch.setattr(pubsub_v1, "SubscriberClient", mock_client_constructor)

    def mock_subscribe(subscription_path, callback=None):
        real_future = real_client.subscribe(
            subscription_path, callback=callback
        )
        mock_future = mock.Mock(spec=real_future, wraps=real_future)

        def mock_result():
            return real_future.result(timeout=10)

        mock_future.result.side_effect = mock_result
        return mock_future

    mock_client.subscribe.side_effect = mock_subscribe

    _publish_messages(topic_path)

    sub.sub(PROJECT, SUBSCRIPTION)

    out, _ = capsys.readouterr()
    assert "Received message" in out
    assert "Acknowledged message" in out
