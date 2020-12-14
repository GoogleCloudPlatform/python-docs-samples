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

import json
import os
import time

import quickstart_createfeed
import quickstart_deletefeed
from google.cloud import resource_manager

json_data = open(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]).read()
data = json.loads(json_data)
PROJECT = data['project_id']
ASSET_NAME = 'assets-{}'.format(int(time.time()))
FEED_ID = 'feed-{}'.format(int(time.time()))
TOPIC = 'topic-{}'.format(int(time.time()))


def test_create_feed(capsys):
    client = resource_manager.Client()
    project_number = client.fetch_project(PROJECT).number
    full_topic_name = "projects/{}/topics/{}".format(PROJECT, TOPIC)
    quickstart_createfeed.create_feed(
        PROJECT, FEED_ID, [ASSET_NAME, ], full_topic_name)
    out, _ = capsys.readouterr()
    if "feed" not in out:
        raise AssertionError

    # Clean up, delete the feed
    feed_name = "projects/{}/feeds/{}".format(project_number, FEED_ID)
    quickstart_deletefeed.delete_feed(feed_name)
