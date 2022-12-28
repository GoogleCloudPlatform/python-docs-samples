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


def get_saved_query(saved_query_name):
    # [START asset_quickstart_get_saved_query]
    from google.cloud import asset_v1

    # TODO saved_query_name = 'SavedQuery Name you want to get'

    client = asset_v1.AssetServiceClient()
    response = client.get_saved_query(request={"name": saved_query_name})
    print(f"gotten_saved_query: {response}")
    # [END asset_quickstart_get_saved_query]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("saved_query_name", help="SavedQuery Name you want to get")
    args = parser.parse_args()
    get_saved_query(args.saved_query_name)
