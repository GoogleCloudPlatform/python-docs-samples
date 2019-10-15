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

import os
import pytest

from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1

import sub


PROJECT = os.environ['GCLOUD_PROJECT']
TOPIC = 'quickstart-sub-test-topic'
SUBSCRIPTION = 'quickstart-sub-test-topic-sub'

publisher_client = pubsub_v1.PublisherClient()
subscriber_client = pubsub_v1.SubscriberClient()


@pytest.fixture(scope='module')
def topic_path():
    topic_path = publisher_client.topic_path(PROJECT, TOPIC)

    try:
        topic = publisher_client.create_topic(topic_path)
        return topic.name
    except AlreadyExists:
        return topic_path


@pytest.fixture(scope='module')
def subscription_path(topic_path):
    subscription_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION)

    try:
        subscription = subscriber_client.create_subscription(
            subscription_path, topic_path)
        return subscription.name
    except AlreadyExists:
        return subscription_path


def _to_delete(resource_paths):
    for item in resource_paths:
        if 'topics' in item:
            publisher_client.delete_topic(item)
        if 'subscriptions' in item:
            subscriber_client.delete_subscription(item)


def _publish_messages(topic_path):
    publish_future = publisher_client.publish(topic_path, data=b'Hello World!')
    publish_future.result()


def _sub_timeout(project_id, subscription_name):
    # This is an exactly copy of `sub.py` except
    # StreamingPullFuture.result() will time out after 10s.
    client = pubsub_v1.SubscriberClient()
    subscription_path = client.subscription_path(
        project_id, subscription_name)

    def callback(message):
        print('Received message {} of message ID {}\n'.format(
            message, message.message_id))
        message.ack()
        print('Acknowledged message {}\n'.format(message.message_id))

    streaming_pull_future = client.subscribe(
        subscription_path, callback=callback)
    print('Listening for messages on {}..\n'.format(subscription_path))

    try:
        streaming_pull_future.result(timeout=10)
    except:  # noqa
        streaming_pull_future.cancel()


def test_sub(monkeypatch, topic_path, subscription_path, capsys):
    monkeypatch.setattr(sub, 'sub', _sub_timeout)

    _publish_messages(topic_path)

    sub.sub(PROJECT, SUBSCRIPTION)

    # Clean up resources.
    _to_delete([topic_path, subscription_path])

    out, _ = capsys.readouterr()
    assert "Received message" in out
    assert "Acknowledged message" in out
