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


def list_feeds(parent_resource):
    # [START asset_quickstart_list_feeds]
    from google.cloud import asset_v1

    # TODO parent_resource = 'Parent resource you want to list all feeds'

    client = asset_v1.AssetServiceClient()
    response = client.list_feeds(request={"parent": parent_resource})
    print("feeds: {}".format(response.feeds))
    # [END asset_quickstart_list_feeds]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "parent_resource", help="Parent resource you want to list all feeds"
    )
    args = parser.parse_args()
    list_feeds(args.parent_resource)
