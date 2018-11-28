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
    from google.cloud import asset_v1beta1
    from google.cloud.asset_v1beta1.proto import assets_pb2
    from google.cloud.asset_v1beta1 import enums

    # TODO project_id = 'Your Google Cloud Project ID'
    # TODO asset_names = 'Your asset names list, e.g.:
    # ["//storage.googleapis.com/[BUCKET_NAME]",]'

    client = asset_v1beta1.AssetServiceClient()
    parent = client.project_path(project_id)
    content_type = enums.ContentType.RESOURCE
    read_time_window = assets_pb2.TimeWindow()
    read_time_window.start_time.GetCurrentTime()
    response = client.batch_get_assets_history(
        parent, content_type, read_time_window, asset_names)
    print('assets: {}'.format(response.assets))
    # [END asset_quickstart_batch_get_assets_history]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('project_id', help='Your Google Cloud project ID')
    parser.add_argument(
        'asset_names',
        help='The asset names for which history will be fetched, comma '
        'delimited, e.g.: //storage.googleapis.com/[BUCKET_NAME]')

    args = parser.parse_args()

    asset_name_list = args.asset_names.split(',')

    batch_get_assets_history(args.project_id, asset_name_list)
