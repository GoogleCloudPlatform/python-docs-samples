#!/usr/bin/env python

# Copyright 2018 Google LLC.
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

import quickstart_createfeed
import quickstart_deletefeed
import quickstart_getfeed
from google.cloud import resource_manager
from google.cloud import pubsub_v1

PROJECT = os.environ['GCLOUD_PROJECT']
ASSET_NAME = 'assets-{}'.format(int(time.time()))
FEED_ID = 'feed-{}'.format(int(time.time()))
TOPIC = 'topic-{}'.format(int(time.time()))


def test_get_feed(capsys):
    client = resource_manager.Client()
    project_number = client.fetch_project(PROJECT).number
    # First create the feed, which will be gotten later
    full_topic_name = "projects/{}/topics/{}".format(PROJECT, TOPIC)
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT, TOPIC)
    publisher.create_topic(topic_path)
    quickstart_createfeed.create_feed(
        PROJECT, FEED_ID, [ASSET_NAME, ], full_topic_name)

    feed_name = "projects/{}/feeds/{}".format(project_number, FEED_ID)
    quickstart_getfeed.get_feed(feed_name)
    out, _ = capsys.readouterr()

    assert "gotten_feed" in out
    # Clean up and delete the feed
    quickstart_deletefeed.delete_feed(feed_name)
    publisher.delete_topic(topic_path)
