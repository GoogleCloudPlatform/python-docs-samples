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
SUBSCRIPTION_ONE = 'subscription-test-subscription-one'
SUBSCRIPTION_TWO = 'subscription-test-subscription-two'
SUBSCRIPTION_THREE = 'subscription-test-subscription-three'
ENDPOINT = 'https://{}.appspot.com/push'.format(PROJECT)
NEW_ENDPOINT = 'https://{}.appspot.com/push2'.format(PROJECT)


@pytest.fixture(scope='module')
def publisher_client():
    yield pubsub_v1.PublisherClient()


@pytest.fixture(scope='module')
def topic(publisher_client):
    topic_path = publisher_client.topic_path(PROJECT, TOPIC)

    try:
        response = publisher_client.get_topic(topic_path)
    except:  # noqa
        response = publisher_client.create_topic(topic_path)

    yield response.name


@pytest.fixture(scope='module')
def subscriber_client():
    yield pubsub_v1.SubscriberClient()


@pytest.fixture(scope='module')
def subscription_one(subscriber_client, topic):
    subscription_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION_ONE)

    try:
        response = subscriber_client.get_subscription(subscription_path)
    except:  # noqa
        response = subscriber_client.create_subscription(
            subscription_path, topic=topic)

    yield response.name


@pytest.fixture(scope='module')
def subscription_two(subscriber_client, topic):
    subscription_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION_TWO)

    try:
        response = subscriber_client.get_subscription(subscription_path)
    except:  # noqa
        response = subscriber_client.create_subscription(
            subscription_path, topic=topic)

    yield response.name


@pytest.fixture(scope='module')
def subscription_three(subscriber_client, topic):
    subscription_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION_THREE)

    try:
        response = subscriber_client.get_subscription(subscription_path)
    except:  # noqa
        response = subscriber_client.create_subscription(
            subscription_path, topic=topic)

    yield response.name


def test_list_in_topic(subscription_one, capsys):
    @eventually_consistent.call
    def _():
        subscriber.list_subscriptions_in_topic(PROJECT, TOPIC)
        out, _ = capsys.readouterr()
        assert subscription_one in out


def test_list_in_project(subscription_one, capsys):
    @eventually_consistent.call
    def _():
        subscriber.list_subscriptions_in_project(PROJECT)
        out, _ = capsys.readouterr()
        assert subscription_one in out


def test_create(subscriber_client):
    subscription_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION_ONE)

    try:
        subscriber_client.delete_subscription(subscription_path)
    except Exception:
        pass

    subscriber.create_subscription(PROJECT, TOPIC, SUBSCRIPTION_ONE)

    @eventually_consistent.call
    def _():
        assert subscriber_client.get_subscription(subscription_path)


def test_create_push(subscriber_client):
    subscription_path = subscriber_client.subscription_path(
        PROJECT, SUBSCRIPTION_ONE)
    try:
        subscriber_client.delete_subscription(subscription_path)
    except Exception:
        pass

    subscriber.create_push_subscription(
        PROJECT, TOPIC, SUBSCRIPTION_ONE, ENDPOINT)

    @eventually_consistent.call
    def _():
        assert subscriber_client.get_subscription(subscription_path)


def test_update(subscriber_client, subscription_one, capsys):
    subscriber.update_subscription(PROJECT, SUBSCRIPTION_ONE, NEW_ENDPOINT)

    out, _ = capsys.readouterr()
    assert 'Subscription updated' in out


def test_delete(subscriber_client, subscription_one):
    subscriber.delete_subscription(PROJECT, SUBSCRIPTION_ONE)

    @eventually_consistent.call
    def _():
        with pytest.raises(Exception):
            subscriber_client.get_subscription(subscription_one)


def _publish_messages(publisher_client, topic):
    for n in range(5):
        data = u'Message {}'.format(n).encode('utf-8')
        future = publisher_client.publish(topic, data=data)
        future.result()


def _publish_messages_with_custom_attributes(publisher_client, topic):
    data = u'Test message'.encode('utf-8')
    future = publisher_client.publish(topic, data=data, origin='python-sample')
    future.result()


def _make_sleep_patch():
    real_sleep = time.sleep

    def new_sleep(period):
        if period == 60:
            real_sleep(5)
            raise RuntimeError('sigil')
        else:
            real_sleep(period)

    return mock.patch('time.sleep', new=new_sleep)


def test_receive(publisher_client, topic, subscription_two, capsys):
    _publish_messages(publisher_client, topic)

    with _make_sleep_patch():
        with pytest.raises(RuntimeError, match='sigil'):
            subscriber.receive_messages(PROJECT, SUBSCRIPTION_TWO)

    out, _ = capsys.readouterr()
    assert 'Listening' in out
    assert subscription_two in out
    assert 'Message 1' in out


def test_receive_with_custom_attributes(
        publisher_client, topic, subscription_two, capsys):

    _publish_messages_with_custom_attributes(publisher_client, topic)

    with _make_sleep_patch():
        with pytest.raises(RuntimeError, match='sigil'):
            subscriber.receive_messages_with_custom_attributes(
                PROJECT, SUBSCRIPTION_TWO)

    out, _ = capsys.readouterr()
    assert 'Test message' in out
    assert 'origin' in out
    assert 'python-sample' in out


def test_receive_with_flow_control(
        publisher_client, topic, subscription_two, capsys):

    _publish_messages(publisher_client, topic)

    with _make_sleep_patch():
        with pytest.raises(RuntimeError, match='sigil'):
            subscriber.receive_messages_with_flow_control(
                PROJECT, SUBSCRIPTION_TWO)

    out, _ = capsys.readouterr()
    assert 'Listening' in out
    assert subscription_two in out
    assert 'Message 1' in out


def test_receive_synchronously(
        publisher_client, topic, subscription_three, capsys):
    _publish_messages(publisher_client, topic)

    subscriber.synchronous_pull(PROJECT, SUBSCRIPTION_THREE)

    out, _ = capsys.readouterr()
    assert 'Done.' in out


def test_receive_synchronously_with_lease(
        publisher_client, topic, subscription_three, capsys):
    _publish_messages(publisher_client, topic)

    subscriber.synchronous_pull_with_lease_management(
        PROJECT, SUBSCRIPTION_THREE)

    out, _ = capsys.readouterr()
    assert 'Done.' in out
