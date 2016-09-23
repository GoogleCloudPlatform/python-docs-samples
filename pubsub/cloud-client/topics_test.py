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

from gcloud import pubsub
from gcp.testing import eventually_consistent
import pytest

import topics

TEST_TOPIC = 'topics-test-topic'


@pytest.fixture
def test_topic():
    client = pubsub.Client()
    topic = client.topic(TEST_TOPIC)
    yield topic
    if topic.exists():
        topic.delete()


def test_list_topics(test_topic, capsys):
    test_topic.create()

    @eventually_consistent.call
    def _():
        topics.list_topics()
        out, _ = capsys.readouterr()
        assert test_topic.name in out


def test_create_topic(test_topic):
    topics.create_topic(test_topic.name)

    @eventually_consistent.call
    def _():
        assert test_topic.exists()


def test_delete_topic(test_topic):
    test_topic.create()

    topics.delete_topic(test_topic.name)

    @eventually_consistent.call
    def _():
        assert not test_topic.exists()


def test_publish_message(test_topic, capsys):
    test_topic.create()

    topics.publish_message(test_topic.name, 'hello')

    out, _ = capsys.readouterr()
    assert 'published' in out


def test_get_topic_policy(test_topic, capsys):
    topics.get_topic_policy(test_topic.name)

    out, _ = capsys.readouterr()
    assert test_topic.name in out


def test_set_topic_policy(test_topic):
    topics.set_topic_policy(test_topic.name)

    policy = test_topic.get_iam_policy()
    assert policy.viewers
    assert policy.editors


def test_test_topic_permissions(test_topic, capsys):
    topics.test_topic_permissions(test_topic.name)

    out, _ = capsys.readouterr()

    assert test_topic.name in out
    assert 'pubsub.topics.publish' in out
