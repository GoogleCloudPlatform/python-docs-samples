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

import os
import pytest
import uuid

from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1

import pub

UUID = uuid.uuid4().hex
PROJECT = os.environ["GCLOUD_PROJECT"]
TOPIC = "quickstart-pub-test-topic-" + UUID


@pytest.fixture(scope="module")
def publisher_client():
    yield pubsub_v1.PublisherClient()


@pytest.fixture(scope="module")
def topic(publisher_client):
    topic_path = publisher_client.topic_path(PROJECT, TOPIC)

    try:
        publisher_client.create_topic(topic_path)
    except AlreadyExists:
        pass

    yield TOPIC

    publisher_client.delete_topic(topic_path)


def test_pub(publisher_client, topic, capsys):
    pub.pub(PROJECT, topic)

    out, _ = capsys.readouterr()

    assert "Hello, World!" in out
