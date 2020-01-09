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
TOPIC_ADMIN = "publisher-test-topic-admin-" + UUID
TOPIC_PUBLISH = "publisher-test-topic-publish-" + UUID


@pytest.fixture
def client():
    yield pubsub_v1.PublisherClient()


@pytest.fixture
def topic_admin(client):
    topic_path = client.topic_path(PROJECT, TOPIC_ADMIN)

    try:
        topic = client.get_topic(topic_path)
    except:  # noqa
        topic = client.create_topic(topic_path)

    yield topic.name
    # Teardown of `topic_admin` is handled in `test_delete()`.


@pytest.fixture
def topic_publish(client):
    topic_path = client.topic_path(PROJECT, TOPIC_PUBLISH)

    try:
        topic = client.get_topic(topic_path)
    except:  # noqa
        topic = client.create_topic(topic_path)

    yield topic.name

    client.delete_topic(topic.name)


def _make_sleep_patch():
    real_sleep = time.sleep

    def new_sleep(period):
        if period == 60:
            real_sleep(5)
            raise RuntimeError("sigil")
        else:
            real_sleep(period)

    return mock.patch("time.sleep", new=new_sleep)


def test_list(client, topic_admin, capsys):
    @eventually_consistent.call
    def _():
        publisher.list_topics(PROJECT)
        out, _ = capsys.readouterr()
        assert topic_admin in out


def test_create(client):
    topic_path = client.topic_path(PROJECT, TOPIC_ADMIN)
    try:
        client.delete_topic(topic_path)
    except Exception:
        pass

    publisher.create_topic(PROJECT, TOPIC_ADMIN)

    @eventually_consistent.call
    def _():
        assert client.get_topic(topic_path)


def test_delete(client, topic_admin):
    publisher.delete_topic(PROJECT, TOPIC_ADMIN)

    @eventually_consistent.call
    def _():
        with pytest.raises(Exception):
            client.get_topic(client.topic_path(PROJECT, TOPIC_ADMIN))


def test_publish(topic_publish, capsys):
    publisher.publish_messages(PROJECT, TOPIC_PUBLISH)

    out, _ = capsys.readouterr()
    assert "Published" in out


def test_publish_with_custom_attributes(topic_publish, capsys):
    publisher.publish_messages_with_custom_attributes(PROJECT, TOPIC_PUBLISH)

    out, _ = capsys.readouterr()
    assert "Published" in out


def test_publish_with_batch_settings(topic_publish, capsys):
    publisher.publish_messages_with_batch_settings(PROJECT, TOPIC_PUBLISH)

    out, _ = capsys.readouterr()
    assert "Published" in out


def test_publish_with_retry_settings(topic_publish, capsys):
    publisher.publish_messages_with_retry_settings(PROJECT, TOPIC_PUBLISH)

    out, _ = capsys.readouterr()
    assert "Published" in out


def test_publish_with_error_handler(topic_publish, capsys):
    publisher.publish_messages_with_error_handler(PROJECT, TOPIC_PUBLISH)

    out, _ = capsys.readouterr()
    assert "Published" in out


def test_publish_with_futures(topic_publish, capsys):
    publisher.publish_messages_with_futures(PROJECT, TOPIC_PUBLISH)

    out, _ = capsys.readouterr()
    assert "Published" in out
