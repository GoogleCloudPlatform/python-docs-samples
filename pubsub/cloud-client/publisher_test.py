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

import publisher

TEST_TOPIC = 'publisher-test-topic'


@pytest.fixture
def test_topic():
    client = pubsub.Client()
    topic = client.topic(TEST_TOPIC)
    yield topic
    if topic.exists():
        topic.delete()


def test_list(test_topic, capsys):
    test_topic.create()

    @eventually_consistent.call
    def _():
        publisher.list_topics()
        out, _ = capsys.readouterr()
        assert test_topic.name in out


def test_create(test_topic):
    publisher.create_topic(test_topic.name)

    @eventually_consistent.call
    def _():
        assert test_topic.exists()


def test_delete(test_topic):
    test_topic.create()

    publisher.delete_topic(test_topic.name)

    @eventually_consistent.call
    def _():
        assert not test_topic.exists()


def test_publish(test_topic, capsys):
    test_topic.create()

    publisher.publish_message(test_topic.name, 'hello')

    out, _ = capsys.readouterr()
    assert 'published' in out
