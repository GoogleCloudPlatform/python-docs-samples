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

from gcp.testing import eventually_consistent
from google.cloud import pubsub
import pytest

import subscriber

TEST_TOPIC = 'subscription-test-topic'
TEST_SUBSCRIPTION = 'subscription-test-subscription'


@pytest.fixture(scope='module')
def test_topic():
    client = pubsub.Client()
    topic = client.topic(TEST_TOPIC)

    if not topic.exists():
        topic.create()

    yield topic

    if topic.exists():
        topic.delete()


@pytest.fixture
def test_subscription(test_topic):
    subscription = test_topic.subscription(TEST_SUBSCRIPTION)
    yield subscription
    if subscription.exists():
        subscription.delete()


def test_list(test_subscription, capsys):
    test_subscription.create()

    @eventually_consistent.call
    def _():
        subscriber.list_subscriptions(test_subscription.topic.name)
        out, _ = capsys.readouterr()
        assert test_subscription.name in out


def test_create(test_subscription):
    subscriber.create_subscription(
        test_subscription.topic.name, test_subscription.name)

    @eventually_consistent.call
    def _():
        assert test_subscription.exists()


def test_delete(test_subscription):
    test_subscription.create()

    subscriber.delete_subscription(
        test_subscription.topic.name, test_subscription.name)

    @eventually_consistent.call
    def _():
        assert not test_subscription.exists()


def test_receive(test_subscription, capsys):
    topic = test_subscription.topic
    test_subscription.create()

    topic.publish('hello'.encode('utf-8'))

    @eventually_consistent.call
    def _():
        subscriber.receive_message(topic.name, test_subscription.name)
        out, _ = capsys.readouterr()
        assert 'hello' in out
