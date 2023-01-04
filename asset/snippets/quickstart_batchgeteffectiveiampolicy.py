#!/usr/bin/env python

# Copyright 2022 Google LLC. All Rights Reserved.
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


def batch_get_effective_iam_policies(resource_names, scope):
    # [START asset_quickstart_batch_get_effective_iam_policies]
    from google.cloud import asset_v1

    # TODO scope = 'project ID/number, folder number or org number'
    # TODO resource_names = 'List of resource names'

    client = asset_v1.AssetServiceClient()

    response = client.batch_get_effective_iam_policies(
      request={"scope": scope, "names": resource_names}
    )
    print(response)
    # [END asset_quickstart_batch_get_effective_iam_policies]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
      description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("resource_names", help="Your specified accessible "
                                               "scope, such as a project, "
                                               "folder or organization")
    parser.add_argument("scope", help="Your specified list of resource names")

    args = parser.parse_args()

    batch_get_effective_iam_policies(args.resource_names, args.scope)
