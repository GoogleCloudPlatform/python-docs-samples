#!/usr/bin/env python

# Copyright 2017 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to get and set IAM policies on Google
Cloud Storage buckets.

For more information, see the documentation at
https://cloud.google.com/storage/docs/access-control/using-iam-permissions.
"""

import argparse

from google.cloud import storage


def view_bucket_iam_members(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy()

    for role in policy:
        members = policy[role]
        print('Role: {}, Members: {}'.format(role, members))


def add_bucket_iam_member(bucket_name, role, member):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy()

    policy[role].add(member)

    bucket.set_iam_policy(policy)

    print('Added {} with role {} to {}.'.format(
         member, role, bucket_name))


def remove_bucket_iam_member(bucket_name, role, member):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy()

    policy[role].discard(member)

    bucket.set_iam_policy(policy)

    print('Removed {} with role {} from {}.'.format(
        member, role, bucket_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('bucket_name', help='Your Cloud Storage bucket name.')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser(
        'view-bucket-iam-members', help=view_bucket_iam_members.__doc__)

    add_member_parser = subparsers.add_parser(
        'add-bucket-iam-member', help=add_bucket_iam_member.__doc__)
    add_member_parser.add_argument('role')
    add_member_parser.add_argument('member')

    remove_member_parser = subparsers.add_parser(
        'remove-bucket-iam-member', help=remove_bucket_iam_member.__doc__)
    remove_member_parser.add_argument('role')
    remove_member_parser.add_argument('member')

    args = parser.parse_args()

    if args.command == 'view-bucket-iam-members':
        view_bucket_iam_members(args.bucket_name)
    elif args.command == 'add-bucket-iam-member':
        add_bucket_iam_member(args.bucket_name, args.role, args.member)
    elif args.command == 'remove-bucket-iam-member':
        remove_bucket_iam_member(args.bucket_name, args.role, args.member)
