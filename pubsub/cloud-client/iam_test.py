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

from google.cloud import pubsub_v1
import pytest

import iam

PROJECT = os.environ['GCLOUD_PROJECT']
TOPIC = 'iam-test-topic'
SUBSCRIPTION = 'iam-test-subscription'


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


def test_get_topic_policy(topic, capsys):
    iam.get_topic_policy(PROJECT, TOPIC)

    out, _ = capsys.readouterr()
    assert topic in out


def test_get_subscription_policy(subscription, capsys):
    iam.get_subscription_policy(PROJECT, SUBSCRIPTION)

    out, _ = capsys.readouterr()
    assert subscription in out


def test_set_topic_policy(publisher_client, topic):
    iam.set_topic_policy(PROJECT, TOPIC)

    policy = publisher_client.get_iam_policy(topic)
    assert 'roles/pubsub.publisher' in str(policy)
    assert 'allUsers' in str(policy)


def test_set_subscription_policy(subscriber_client, subscription):
    iam.set_subscription_policy(PROJECT, SUBSCRIPTION)

    policy = subscriber_client.get_iam_policy(subscription)
    assert 'roles/pubsub.viewer' in str(policy)
    assert 'allUsers' in str(policy)


def test_check_topic_permissions(topic, capsys):
    iam.check_topic_permissions(PROJECT, TOPIC)

    out, _ = capsys.readouterr()

    assert topic in out
    assert 'pubsub.topics.publish' in out


def test_check_subscription_permissions(subscription, capsys):
    iam.check_subscription_permissions(PROJECT, SUBSCRIPTION)

    out, _ = capsys.readouterr()

    assert subscription in out
    assert 'pubsub.subscriptions.consume' in out
