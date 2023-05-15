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
import uuid

import quickstart_createfeed


PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
ASSET_NAME = f"assets-{uuid.uuid4().hex}"
FEED_ID = f"feed-{uuid.uuid4().hex}"
FEED_ID_R = f"feed-{uuid.uuid4().hex}"


def test_create_feed(capsys, test_topic, deleter):
    from google.cloud import asset_v1

    feed = quickstart_createfeed.create_feed(
        PROJECT, FEED_ID, [ASSET_NAME], test_topic.name,
        asset_v1.ContentType.RESOURCE)
    deleter.append(feed.name)
    out, _ = capsys.readouterr()
    assert "feed" in out

    feed_r = quickstart_createfeed.create_feed(
        PROJECT, FEED_ID_R, [ASSET_NAME], test_topic.name,
        asset_v1.ContentType.RELATIONSHIP)
    deleter.append(feed_r.name)
    out_r, _ = capsys.readouterr()
    assert "feed" in out_r
