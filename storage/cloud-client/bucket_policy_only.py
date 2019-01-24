#!/usr/bin/env python

# Copyright 2019 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
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

from google.cloud import storage


def enable_bucket_policy_only(bucket_name):
    """Enable Bucket Policy Only for a bucket"""
    # [START storage_enable_bucket_policy_only]
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    bucket.iam_configuration.bucket_policy_only_enabled = True
    bucket.patch()

    print('Bucket Policy Only was enabled for {}.'.format(bucket.name))
    # [END storage_enable_bucket_policy_only]


def disable_bucket_policy_only(bucket_name):
    """Disable Bucket Policy Only for a bucket"""
    # [START storage_disable_bucket_policy_only]
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    bucket.iam_configuration.bucket_policy_only_enabled = False
    bucket.patch()

    print('Bucket Policy Only was disabled for {}.'.format(bucket.name))
    # [END storage_disable_bucket_policy_only]


def get_bucket_policy_only(bucket_name):
    """Get Bucket Policy Only for a bucket"""
    # [START storage_get_bucket_policy_only]
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    iam_configuration = bucket.iam_configuration

    if iam_configuration.bucket_policy_only_enabled:
        print('Bucket Policy Only is enabled for {}.'.format(bucket.name))
        print('Bucket will be locked on {}.'.format(
            iam_configuration.bucket_policy_only_locked_time))
    else:
        print('Bucket Policy Only is disabled for {}.'.format(bucket.name))
    # [END storage_get_bucket_policy_only]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    enable_bucket_policy_only_parser = subparsers.add_parser(
        'enable-bucket-policy-only', help=enable_bucket_policy_only.__doc__)
    enable_bucket_policy_only_parser.add_argument('bucket_name')

    disable_bucket_policy_only_parser = subparsers.add_parser(
        'disable-bucket-policy-only', help=disable_bucket_policy_only.__doc__)
    disable_bucket_policy_only_parser.add_argument('bucket_name')

    get_bucket_policy_only_parser = subparsers.add_parser(
        'get-bucket-policy-only', help=get_bucket_policy_only.__doc__)
    get_bucket_policy_only_parser.add_argument('bucket_name')

    args = parser.parse_args()

    if args.command == 'enable-bucket-policy-only':
        enable_bucket_policy_only(args.bucket_name)
    elif args.command == 'disable-bucket-policy-only':
        disable_bucket_policy_only(args.bucket_name)
    elif args.command == 'get-bucket-policy-only':
        get_bucket_policy_only(args.bucket_name)
