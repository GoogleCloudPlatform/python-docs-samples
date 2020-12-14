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
import quickstart_updatefeed
from google.cloud import resource_manager

PROJECT = os.environ['GCLOUD_PROJECT']
ASSET_NAME = 'assets-{}'.format(int(time.time()))
FEED_ID = 'feed-{}'.format(int(time.time()))
TOPIC = 'topic-{}'.format(int(time.time()))
NEW_TOPIC = 'new-topic-{}'.format(int(time.time()))


def test_update_feed(capsys):
    client = resource_manager.Client()
    project_number = client.fetch_project(PROJECT).number
    # First create the feed, which will be updated later
    full_topic_name = "projects/{}/topics/{}".format(PROJECT, TOPIC)
    quickstart_createfeed.create_feed(
        PROJECT, FEED_ID, [ASSET_NAME, ], full_topic_name)

    feed_name = "projects/{}/feeds/{}".format(project_number, FEED_ID)
    new_full_topic_name = "projects/" + PROJECT + "/topics/" + NEW_TOPIC
    quickstart_updatefeed.update_feed(feed_name, new_full_topic_name)
    out, _ = capsys.readouterr()

    if "updated_feed" not in out:
        raise AssertionError
    # Clean up and delete the feed
    quickstart_deletefeed.delete_feed(feed_name)
