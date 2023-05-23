#!/usr/bin/env python

# Copyright 2019 Google LLC.
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


import argparse


def create_feed(project_id, feed_id, asset_names, topic, content_type):
    # [START asset_quickstart_create_feed]
    from google.cloud import asset_v1

    # TODO project_id = 'Your Google Cloud Project ID'
    # TODO feed_id = 'Feed ID you want to create'
    # TODO asset_names = 'List of asset names the feed listen to'
    # TODO topic = "Topic name of the feed"
    # TODO content_type ="Content type of the feed"

    client = asset_v1.AssetServiceClient()
    parent = f"projects/{project_id}"
    feed = asset_v1.Feed()
    feed.asset_names.extend(asset_names)
    feed.feed_output_config.pubsub_destination.topic = topic
    feed.content_type = content_type
    response = client.create_feed(
        request={"parent": parent, "feed_id": feed_id, "feed": feed}
    )
    print(f"feed: {response}")
    # [END asset_quickstart_create_feed]
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID")
    parser.add_argument("feed_id", help="Feed ID you want to create")
    parser.add_argument("asset_names", help="List of asset names the feed listen to")
    parser.add_argument("topic", help="Topic name of the feed")
    parser.add_argument("content_type", help="Content type of the feed")
    args = parser.parse_args()
    create_feed(args.project_id, args.feed_id, args.asset_names, args.topic, args.content_type)
