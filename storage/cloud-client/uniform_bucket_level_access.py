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


def enable_uniform_bucket_level_access(bucket_name):
    """Enable uniform bucket-level access for a bucket"""
    # [START storage_enable_uniform_bucket_level_access]
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    bucket.patch()

    print('Uniform bucket-level access was enabled for {}.'.format(
        bucket.name))
    # [END storage_enable_uniform_bucket_level_access]


def disable_uniform_bucket_level_access(bucket_name):
    """Disable uniform bucket-level access for a bucket"""
    # [START storage_disable_uniform_bucket_level_access]
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    bucket.iam_configuration.uniform_bucket_level_access_enabled = False
    bucket.patch()

    print('Uniform bucket-level access was disabled for {}.'.format(
        bucket.name))
    # [END storage_disable_uniform_bucket_level_access]


def get_uniform_bucket_level_access(bucket_name):
    """Get uniform bucket-level access for a bucket"""
    # [START storage_get_uniform_bucket_level_access]
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    iam_configuration = bucket.iam_configuration

    if iam_configuration.uniform_bucket_level_access_enabled:
        print('Uniform bucket-level access is enabled for {}.'.format(
            bucket.name))
        print('Bucket will be locked on {}.'.format(
            iam_configuration.uniform_bucket_level_locked_time))
    else:
        print('Uniform bucket-level access is disabled for {}.'.format(
            bucket.name))
    # [END storage_get_uniform_bucket_level_access]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    enable_uniform_bucket_level_access_parser = subparsers.add_parser(
        'enable-uniform-bucket-level-access',
        help=enable_uniform_bucket_level_access.__doc__)
    enable_uniform_bucket_level_access_parser.add_argument('bucket_name')

    disable_uniform_bucket_level_access_parser = subparsers.add_parser(
        'disable-uniform-bucket-level-access',
        help=disable_uniform_bucket_level_access.__doc__)
    disable_uniform_bucket_level_access_parser.add_argument('bucket_name')

    get_uniform_bucket_level_access_parser = subparsers.add_parser(
        'get-uniform-bucket-level-access',
        help=get_uniform_bucket_level_access.__doc__)
    get_uniform_bucket_level_access_parser.add_argument('bucket_name')

    args = parser.parse_args()

    if args.command == 'enable-uniform-bucket-level-access':
        enable_uniform_bucket_level_access(args.bucket_name)
    elif args.command == 'disable-uniform-bucket-level-access':
        disable_uniform_bucket_level_access(args.bucket_name)
    elif args.command == 'get-uniform-bucket-level-access':
        get_uniform_bucket_level_access(args.bucket_name)
