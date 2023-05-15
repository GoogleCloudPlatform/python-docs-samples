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


def get_feed(feed_name):
    # [START asset_quickstart_get_feed]
    from google.cloud import asset_v1

    # TODO feed_name = 'Feed Name you want to get'

    client = asset_v1.AssetServiceClient()
    response = client.get_feed(request={"name": feed_name})
    print(f"gotten_feed: {response}")
    # [END asset_quickstart_get_feed]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("feed_name", help="Feed Name you want to get")
    args = parser.parse_args()
    get_feed(args.feed_name)
