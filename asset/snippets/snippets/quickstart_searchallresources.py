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


def search_all_resources(scope,
                         query=None,
                         asset_types=None,
                         page_size=None,
                         order_by=None):
    # [START asset_quickstart_search_all_resources]
    from google.cloud import asset_v1

    client = asset_v1.AssetServiceClient()
    response = client.search_all_resources(
        scope,
        query=query,
        asset_types=asset_types,
        page_size=page_size,
        order_by=order_by)
    for page in response.pages:
        for resource in page:
            print(resource)
        break
    # [END asset_quickstart_search_all_resources]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'scope',
        help='The search is limited to the resources within the scope.')
    parser.add_argument('--query', help='The query statement.')
    parser.add_argument(
        '--asset_types', nargs='+', help='A list of asset types to search for.')
    parser.add_argument(
        '--page_size',
        type=int,
        help='The page size for search result pagination.')
    parser.add_argument(
        '--order_by',
        help='Fields specifying the sorting order of the results.')
    args = parser.parse_args()
    search_all_resources(args.scope, args.query, args.asset_types,
                         args.page_size, args.order_by)
