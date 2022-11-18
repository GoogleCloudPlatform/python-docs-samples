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


def update_saved_query(saved_query_name, description):
    # [START asset_quickstart_update_saved_query]
    from google.cloud import asset_v1
    from google.protobuf import field_mask_pb2

    # TODO saved_query_name = 'SavedQuery Name you want to update'
    # TODO description = "New description'

    client = asset_v1.AssetServiceClient()
    saved_query = asset_v1.SavedQuery()
    saved_query.name = saved_query_name
    saved_query.description = description
    update_mask = field_mask_pb2.FieldMask()
    # In this example, we only update description of the saved_query.
    # You can update other content of the saved query.
    update_mask.paths.append("description")
    response = client.update_saved_query(request={"saved_query": saved_query, "update_mask": update_mask})
    print(f"updated_saved_query: {response}")
    # [END asset_quickstart_update_saved_query]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("saved_query_name", help="SavedQuery Name you want to update")
    parser.add_argument("description", help="The description you want to update with")
    args = parser.parse_args()
    update_saved_query(args.saved_query_name, args.description)
