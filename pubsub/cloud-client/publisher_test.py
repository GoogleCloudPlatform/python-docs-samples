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
import uuid

from gcp_devrel.testing import eventually_consistent
from google.cloud import pubsub_v1
import mock
import pytest

import publisher

UUID = uuid.uuid4().hex
PROJECT = os.environ["GCLOUD_PROJECT"]
TOPIC_ONE = "publisher-test-topic-one-" + UUID
TOPIC_TWO = "publisher-test-topic-two-" + UUID


@pytest.fixture
def client():
    yield pubsub_v1.PublisherClient()


@pytest.fixture
def topic_one(client):
    topic_path = client.topic_path(PROJECT, TOPIC_ONE)

    try:
        response = client.get_topic(topic_path)
    except:  # noqa
        response = client.create_topic(topic_path)

    yield response.name


@pytest.fixture
def topic_two(client):
    topic_path = client.topic_path(PROJECT, TOPIC_TWO)

    try:
        response = client.get_topic(topic_path)
    except:  # noqa
        response = client.create_topic(topic_path)

    yield response.name

    client.delete_topic(response.name)


def _make_sleep_patch():
    real_sleep = time.sleep

    def new_sleep(period):
        if period == 60:
            real_sleep(5)
            raise RuntimeError("sigil")
        else:
            real_sleep(period)

    return mock.patch("time.sleep", new=new_sleep)


def test_list(client, topic_one, capsys):
    @eventually_consistent.call
    def _():
        publisher.list_topics(PROJECT)
        out, _ = capsys.readouterr()
        assert topic_one in out


def test_create(client):
    topic_path = client.topic_path(PROJECT, TOPIC_ONE)
    try:
        client.delete_topic(topic_path)
    except Exception:
        pass

    publisher.create_topic(PROJECT, TOPIC_ONE)

    @eventually_consistent.call
    def _():
        assert client.get_topic(topic_path)


def test_delete(client, topic_one):
    publisher.delete_topic(PROJECT, TOPIC_ONE)

    @eventually_consistent.call
    def _():
        with pytest.raises(Exception):
            client.get_topic(client.topic_path(PROJECT, TOPIC_ONE))


def test_publish(topic_two, capsys):
    publisher.publish_messages(PROJECT, TOPIC_TWO)

    out, _ = capsys.readouterr()
    assert "Published" in out


def test_publish_with_custom_attributes(topic_two, capsys):
    publisher.publish_messages_with_custom_attributes(PROJECT, TOPIC_TWO)

    out, _ = capsys.readouterr()
    assert "Published" in out


def test_publish_with_batch_settings(topic_two, capsys):
    publisher.publish_messages_with_batch_settings(PROJECT, TOPIC_TWO)

    out, _ = capsys.readouterr()
    assert "Published" in out


def test_publish_with_retry_settings(topic_two, capsys):
    publisher.publish_messages_with_retry_settings(PROJECT, TOPIC_TWO)

    out, _ = capsys.readouterr()
    assert "Published" in out


def test_publish_with_error_handler(topic_two, capsys):
    publisher.publish_messages_with_error_handler(PROJECT, TOPIC_TWO)

    out, _ = capsys.readouterr()
    assert "Published" in out


def test_publish_with_futures(topic_two, capsys):
    publisher.publish_messages_with_futures(PROJECT, TOPIC_TWO)

    out, _ = capsys.readouterr()
    assert "Published" in out
