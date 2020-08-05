#!/usr/bin/env python

# Copyright 2020 Google LLC.
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


def search_all_iam_policies(scope, query=None, page_size=None):
    # [START asset_quickstart_search_all_iam_policies]
    from google.cloud import asset_v1

    # TODO scope = 'Scope of the search'
    # TODO query = 'Query statement'
    # TODO page_size = Size of each result page

    client = asset_v1.AssetServiceClient()
    response = client.search_all_iam_policies(
        request={"scope": scope, "query": query, "page_size": page_size}
    )
    for policy in response:
        print(policy)
        break
    # [END asset_quickstart_search_all_iam_policies]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "scope", help="The search is limited to the resources within the scope."
    )
    parser.add_argument("--query", help="The query statement.")
    parser.add_argument(
        "--page_size", type=int, help="The page size for search result pagination."
    )
    args = parser.parse_args()
    search_all_iam_policies(args.scope, args.query, args.page_size)
