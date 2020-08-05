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


def batch_get_assets_history(project_id, asset_names):
    # [START asset_quickstart_batch_get_assets_history]
    from google.cloud import asset_v1

    # TODO project_id = 'Your Google Cloud Project ID'
    # TODO asset_names = 'Your asset names list, e.g.:
    # ["//storage.googleapis.com/[BUCKET_NAME]",]'

    client = asset_v1.AssetServiceClient()
    parent = "projects/{}".format(project_id)
    content_type = asset_v1.ContentType.RESOURCE
    read_time_window = asset_v1.TimeWindow()
    response = client.batch_get_assets_history(
        request={
            "parent": parent,
            "asset_names": asset_names,
            "content_type": content_type,
            "read_time_window": read_time_window,
        }
    )
    print("assets: {}".format(response.assets))
    # [END asset_quickstart_batch_get_assets_history]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID")
    parser.add_argument(
        "asset_names",
        help="The asset names for which history will be fetched, comma "
        "delimited, e.g.: //storage.googleapis.com/[BUCKET_NAME]",
    )

    args = parser.parse_args()

    asset_name_list = args.asset_names.split(",")

    batch_get_assets_history(args.project_id, asset_name_list)
