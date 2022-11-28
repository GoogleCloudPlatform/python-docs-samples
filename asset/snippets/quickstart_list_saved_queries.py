#!/usr/bin/env python

# Copyright 2022 Google LLC.
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


def list_saved_queries(parent_resource):
    # [START asset_quickstart_list_saved_queries]
    from google.cloud import asset_v1

    # TODO parent_resource = 'Parent resource you want to list all saved_queries'

    client = asset_v1.AssetServiceClient()
    response = client.list_saved_queries(request={"parent": parent_resource})
    print(f"saved_queries: {response.saved_queries}")
    # [END asset_quickstart_list_saved_queries]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "parent_resource", help="Parent resource you want to list all saved_queries"
    )
    args = parser.parse_args()
    list_saved_queries(args.parent_resource)
