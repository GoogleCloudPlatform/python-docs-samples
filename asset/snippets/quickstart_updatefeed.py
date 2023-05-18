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


import argparse


def update_feed(feed_name, topic):
    # [START asset_quickstart_update_feed]
    from google.cloud import asset_v1
    from google.protobuf import field_mask_pb2

    # TODO feed_name = 'Feed Name you want to update'
    # TODO topic = "Topic name you want to update with"

    client = asset_v1.AssetServiceClient()
    feed = asset_v1.Feed()
    feed.name = feed_name
    feed.feed_output_config.pubsub_destination.topic = topic
    update_mask = field_mask_pb2.FieldMask()
    # In this example, we update topic of the feed
    update_mask.paths.append("feed_output_config.pubsub_destination.topic")
    response = client.update_feed(request={"feed": feed, "update_mask": update_mask})
    print(f"updated_feed: {response}")
    # [END asset_quickstart_update_feed]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("feed_name", help="Feed Name you want to update")
    parser.add_argument("topic", help="Topic name you want to update with")
    args = parser.parse_args()
    update_feed(args.feed_name, args.topic)
