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

from google.cloud import pubsub
import pytest

import iam

TEST_TOPIC = 'iam-test-topic'
TEST_SUBSCRIPTION = 'iam-test-subscription'


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


def test_get_topic_policy(test_topic, capsys):
    iam.get_topic_policy(test_topic.name)

    out, _ = capsys.readouterr()
    assert test_topic.name in out


def test_get_subscription_policy(test_subscription, capsys):
    test_subscription.create()

    iam.get_subscription_policy(
        test_subscription.topic.name,
        test_subscription.name)

    out, _ = capsys.readouterr()
    assert test_subscription.topic.name in out
    assert test_subscription.name in out


def test_set_topic_policy(test_topic):
    iam.set_topic_policy(test_topic.name)

    policy = test_topic.get_iam_policy()
    assert policy.viewers
    assert policy.editors


def test_set_subscription_policy(test_subscription):
    test_subscription.create()

    iam.set_subscription_policy(
        test_subscription.topic.name,
        test_subscription.name)

    policy = test_subscription.get_iam_policy()
    assert policy.viewers
    assert policy.editors


def test_check_topic_permissions(test_topic, capsys):
    iam.check_topic_permissions(test_topic.name)

    out, _ = capsys.readouterr()

    assert test_topic.name in out
    assert 'pubsub.topics.publish' in out


def test_check_subscription_permissions(test_subscription, capsys):
    test_subscription.create()

    iam.check_subscription_permissions(
        test_subscription.topic.name,
        test_subscription.name)

    out, _ = capsys.readouterr()

    assert test_subscription.topic.name in out
    assert test_subscription.name in out
    assert 'pubsub.subscriptions.consume' in out
