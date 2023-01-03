#!/usr/bin/env python
#
# Copyright 2020 Google LLC
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
import uuid

import backoff
from google.api_core.exceptions import InternalServerError
from google.api_core.exceptions import NotFound
from google.cloud import pubsub_v1
import pytest

import quickstart_create_saved_query
import quickstart_createfeed
import quickstart_delete_saved_query
import quickstart_deletefeed


PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="module")
def test_topic():
    topic_id = f"topic-{uuid.uuid4().hex}"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT, topic_id)
    topic = publisher.create_topic(request={"name": topic_path})

    yield topic

    publisher.delete_topic(request={"topic": topic_path})


@pytest.fixture(scope="module")
def another_topic():
    topic_id = f"topic-{uuid.uuid4().hex}"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT, topic_id)
    topic = publisher.create_topic(request={"name": topic_path})

    yield topic

    publisher.delete_topic(request={"topic": topic_path})


@pytest.fixture(scope="module")
def test_feed(test_topic):
    from google.cloud import asset_v1

    feed_id = f"feed-{uuid.uuid4().hex}"
    asset_name = f"assets-{uuid.uuid4().hex}"

    @backoff.on_exception(backoff.expo, InternalServerError, max_time=60)
    def create_feed():
        return quickstart_createfeed.create_feed(
            PROJECT, feed_id, [asset_name], test_topic.name, asset_v1.ContentType.RESOURCE
        )

    feed = create_feed()

    yield feed

    try:
        quickstart_deletefeed.delete_feed(feed.name)
    except NotFound as e:
        print(f"Ignoring NotFound: {e}")


@pytest.fixture(scope="module")
def deleter():
    feeds_to_delete = []

    yield feeds_to_delete

    for feed_name in feeds_to_delete:
        try:
            quickstart_deletefeed.delete_feed(feed_name)
        except NotFound as e:
            print(f"Ignoring NotFound: {e}")


@pytest.fixture(scope="module")
def test_saved_query():
    saved_query_id = f"saved-query-{uuid.uuid4().hex}"

    @backoff.on_exception(backoff.expo, InternalServerError, max_time=60)
    def create_saved_query():
        return quickstart_create_saved_query.create_saved_query(
            PROJECT, saved_query_id, "description foo"
        )

    saved_query = create_saved_query()

    yield saved_query

    try:
        quickstart_delete_saved_query.delete_saved_query(saved_query.name)
    except NotFound as e:
        print(f"Ignoring NotFound: {e}")


@pytest.fixture(scope="module")
def saved_query_deleter():
    saved_querys_to_delete = []

    yield saved_querys_to_delete

    for saved_query_name in saved_querys_to_delete:
        try:
            quickstart_delete_saved_query.delete_saved_query(saved_query_name)
        except NotFound as e:
            print(f"Ignoring NotFound: {e}")
