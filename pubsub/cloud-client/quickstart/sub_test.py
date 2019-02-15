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
import time

from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1

import sub


PROJECT = os.environ['GCLOUD_PROJECT']
TOPIC = 'quickstart-sub-test-topic'
SUBSCRIPTION = 'quickstart-sub-test-topic-sub'


@pytest.fixture(scope='module')
def publisher_client():
    yield pubsub_v1.PublisherClient()


@pytest.fixture(scope='module')
def topic_path(publisher_client):
    topic_path = publisher_client.topic_path(PROJECT, TOPIC)

    try:
        publisher_client.create_topic(topic_path)
    except AlreadyExists:
        pass

    yield topic_path


@pytest.fixture(scope='module')
def subscriber_client():
    yield pubsub_v1.SubscriberClient()


@pytest.fixture(scope='module')
def subscription(subscriber_client, topic_path):
    subscription_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION)

    try:
        subscriber_client.create_subscription(subscription_path, topic_path)
    except AlreadyExists:
        pass

    yield SUBSCRIPTION


@pytest.fixture
def to_delete(publisher_client, subscriber_client):
    doomed = []
    yield doomed
    for client, item in doomed:
        if 'topics' in item:
            publisher_client.delete_topic(item)
        if 'subscriptions' in item:
            subscriber_client.delete_subscription(item)


def _make_sleep_patch():
    real_sleep = time.sleep

    def new_sleep(period):
        if period == 60:
            real_sleep(10)
            raise RuntimeError('sigil')
        else:
            real_sleep(period)

    return mock.patch('time.sleep', new=new_sleep)


def test_sub(publisher_client,
             topic_path,
             subscriber_client,
             subscription,
             to_delete,
             capsys):

    publisher_client.publish(topic_path, data=b'Hello, World!')

    to_delete.append((publisher_client, topic_path))

    with _make_sleep_patch():
        with pytest.raises(RuntimeError, match='sigil'):
            sub.sub(PROJECT, subscription)

    to_delete.append((subscriber_client,
                      'projects/{}/subscriptions/{}'.format(PROJECT,
                                                            SUBSCRIPTION)))

    out, _ = capsys.readouterr()
    assert "Received message" in out
    assert "Acknowledged message" in out
