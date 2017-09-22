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
import time

from gcp_devrel.testing import eventually_consistent
from google.cloud import pubsub_v1
import mock
import pytest

import subscriber

PROJECT = os.environ['GCLOUD_PROJECT']
TOPIC = 'subscription-test-topic'
SUBSCRIPTION = 'subscription-test-subscription'


@pytest.fixture(scope='module')
def publisher_client():
    yield pubsub_v1.PublisherClient()


@pytest.fixture(scope='module')
def topic(publisher_client):
    topic_path = publisher_client.topic_path(PROJECT, TOPIC)

    try:
        publisher_client.delete_topic(topic_path)
    except:
        pass

    publisher_client.create_topic(topic_path)

    yield topic_path


@pytest.fixture(scope='module')
def subscriber_client():
    yield pubsub_v1.SubscriberClient()


@pytest.fixture
def subscription(subscriber_client, topic):
    subscription_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION)

    try:
        subscriber_client.delete_subscription(subscription_path)
    except:
        pass

    subscriber_client.create_subscription(subscription_path, topic=topic)

    yield subscription_path


def test_list(subscription, capsys):
    @eventually_consistent.call
    def _():
        subscriber.list_subscriptions(PROJECT, TOPIC)
        out, _ = capsys.readouterr()
        assert subscription in out


def test_create(subscriber_client):
    subscription_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION)
    try:
        subscriber_client.delete_subscription(subscription_path)
    except:
        pass

    subscriber.create_subscription(PROJECT, TOPIC, SUBSCRIPTION)

    @eventually_consistent.call
    def _():
        assert subscriber_client.get_subscription(subscription_path)


def test_delete(subscriber_client, subscription):
    subscriber.delete_subscription(PROJECT, SUBSCRIPTION)

    @eventually_consistent.call
    def _():
        with pytest.raises(Exception):
            subscriber_client.get_subscription(subscription)


def _publish_messages(publisher_client, topic):
    for n in range(5):
        data = u'Message {}'.format(n).encode('utf-8')
        publisher_client.publish(
            topic, data=data)


def _make_sleep_patch():
    real_sleep = time.sleep

    def new_sleep(period):
        if period == 60:
            real_sleep(5)
            raise RuntimeError('sigil')
        else:
            real_sleep(period)

    return mock.patch('time.sleep', new=new_sleep)


def test_receive(publisher_client, topic, subscription, capsys):
    _publish_messages(publisher_client, topic)

    with _make_sleep_patch():
        with pytest.raises(RuntimeError, match='sigil'):
            subscriber.receive_messages(PROJECT, SUBSCRIPTION)

    out, _ = capsys.readouterr()
    assert 'Listening' in out
    assert subscription in out
    assert 'Message 1' in out


def test_receive_with_flow_control(
        publisher_client, topic, subscription, capsys):
    _publish_messages(publisher_client, topic)

    with _make_sleep_patch():
        with pytest.raises(RuntimeError, match='sigil'):
            subscriber.receive_messages_with_flow_control(
                PROJECT, SUBSCRIPTION)

    out, _ = capsys.readouterr()
    assert 'Listening' in out
    assert subscription in out
    assert 'Message 1' in out
