#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
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


def set_retention_policy(bucket_name, retention_period):
    """Defines a retention policy on a given bucket"""
    # [START storage_set_retention_policy]
    # bucket_name = "my-bucket"
    # retention_period = 10

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    bucket.retention_period = retention_period
    bucket.patch()

    print('Bucket {} retention period set for {} seconds'.format(
        bucket.name,
        bucket.retention_period))
    # [END storage_set_retention_policy]


def remove_retention_policy(bucket_name):
    """Removes the retention policy on a given bucket"""
    # [START storage_remove_retention_policy]
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    bucket.reload()

    if bucket.retention_policy_locked:
        print(
            'Unable to remove retention period as retention policy is locked.')
        return

    bucket.retention_period = None
    bucket.patch()

    print('Removed bucket {} retention policy'.format(bucket.name))
    # [END storage_remove_retention_policy]


def lock_retention_policy(bucket_name):
    """Locks the retention policy on a given bucket"""
    # [START storage_lock_retention_policy]
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    # get_bucket gets the current metageneration value for the bucket,
    # required by lock_retention_policy.
    bucket = storage_client.get_bucket(bucket_name)

    # Warning: Once a retention policy is locked it cannot be unlocked
    # and retention period can only be increased.
    bucket.lock_retention_policy()

    print('Retention policy for {} is now locked'.format(bucket_name))
    print('Retention policy effective as of {}'.format(
        bucket.retention_policy_effective_time))
    # [END storage_lock_retention_policy]


def get_retention_policy(bucket_name):
    """Gets the retention policy on a given bucket"""
    # [START storage_get_retention_policy]
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    bucket.reload()

    print('Retention Policy for {}'.format(bucket_name))
    print('Retention Period: {}'.format(bucket.retention_period))
    if bucket.retention_policy_locked:
        print('Retention Policy is locked')

    if bucket.retention_policy_effective_time:
        print('Effective Time: {}'
              .format(bucket.retention_policy_effective_time))
    # [END storage_get_retention_policy]


def set_temporary_hold(bucket_name, blob_name):
    """Sets a temporary hold on a given blob"""
    # [START storage_set_temporary_hold]
    # bucket_name = "my-bucket"
    # blob_name = "my-blob"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.temporary_hold = True
    blob.patch()

    print("Temporary hold was set for #{blob_name}")
    # [END storage_set_temporary_hold]


def release_temporary_hold(bucket_name, blob_name):
    """Releases the temporary hold on a given blob"""
    # [START storage_release_temporary_hold]
    # bucket_name = "my-bucket"
    # blob_name = "my-blob"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.temporary_hold = False
    blob.patch()

    print("Temporary hold was release for #{blob_name}")
    # [END storage_release_temporary_hold]


def set_event_based_hold(bucket_name, blob_name):
    """Sets a event based hold on a given blob"""
    # [START storage_set_event_based_hold]
    # bucket_name = "my-bucket"
    # blob_name = "my-blob"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.event_based_hold = True
    blob.patch()

    print('Event based hold was set for {}'.format(blob_name))
    # [END storage_set_event_based_hold]


def release_event_based_hold(bucket_name, blob_name):
    """Releases the event based hold on a given blob"""
    # [START storage_release_event_based_hold]
    # bucket_name = "my-bucket"
    # blob_name = "my-blob"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.event_based_hold = False
    blob.patch()

    print('Event based hold was released for {}'.format(blob_name))
    # [END storage_release_event_based_hold]


def enable_default_event_based_hold(bucket_name):
    """Enables the default event based hold on a given bucket"""
    # [START storage_enable_default_event_based_hold]
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    bucket.default_event_based_hold = True
    bucket.patch()

    print('Default event based hold was enabled for {}'.format(bucket_name))
    # [END storage_enable_default_event_based_hold]


def disable_default_event_based_hold(bucket_name):
    """Disables the default event based hold on a given bucket"""
    # [START storage_disable_default_event_based_hold]
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    bucket.default_event_based_hold = False
    bucket.patch()

    print("Default event based hold was disabled for {}".format(bucket_name))
    # [END storage_disable_default_event_based_hold]


def get_default_event_based_hold(bucket_name):
    """Gets the default event based hold on a given bucket"""
    # [START storage_get_default_event_based_hold]
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    bucket.reload()

    if bucket.default_event_based_hold:
        print('Default event-based hold is enabled for {}'.format(bucket_name))
    else:
        print('Default event-based hold is not enabled for {}'
              .format(bucket_name))
    # [END storage_get_default_event_based_hold]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    set_retention_policy_parser = subparsers.add_parser(
        'set-retention-policy', help=set_retention_policy.__doc__)
    set_retention_policy_parser.add_argument('bucket_name')
    set_retention_policy_parser.add_argument('retention_period')

    remove_retention_policy_parser = subparsers.add_parser(
        'remove-retention-policy', help=remove_retention_policy.__doc__)
    remove_retention_policy_parser.add_argument('bucket_name')

    lock_retention_policy_parser = subparsers.add_parser(
        'lock-retention-policy', help=lock_retention_policy.__doc__)
    lock_retention_policy_parser.add_argument('bucket_name')

    get_retention_policy_parser = subparsers.add_parser(
        'get-retention-policy', help=get_retention_policy.__doc__)
    get_retention_policy_parser.add_argument('bucket_name')

    set_temporary_hold_parser = subparsers.add_parser(
        'set-temporary-hold', help=set_temporary_hold.__doc__)
    set_temporary_hold_parser.add_argument('bucket_name')
    set_temporary_hold_parser.add_argument('blob_name')

    release_temporary_hold_parser = subparsers.add_parser(
        'release-temporary-hold', help=release_temporary_hold.__doc__)
    release_temporary_hold_parser.add_argument('bucket_name')
    release_temporary_hold_parser.add_argument('blob_name')

    set_event_based_hold_parser = subparsers.add_parser(
        'set-event-based-hold', help=set_event_based_hold.__doc__)
    set_event_based_hold_parser.add_argument('bucket_name')
    set_event_based_hold_parser.add_argument('blob_name')

    release_event_based_hold_parser = subparsers.add_parser(
        'release-event-based-hold', help=release_event_based_hold.__doc__)
    release_event_based_hold_parser.add_argument('bucket_name')
    release_event_based_hold_parser.add_argument('blob_name')

    enable_default_event_based_hold_parser = subparsers.add_parser(
        'enable-default-event-based-hold',
        help=enable_default_event_based_hold.__doc__)
    enable_default_event_based_hold_parser.add_argument('bucket_name')

    disable_default_event_based_hold_parser = subparsers.add_parser(
        'disable-default-event-based-hold',
        help=disable_default_event_based_hold.__doc__)
    disable_default_event_based_hold_parser.add_argument('bucket_name')

    get_default_event_based_hold_parser = subparsers.add_parser(
        'get-default-event-based-hold',
        help=get_default_event_based_hold.__doc__)
    get_default_event_based_hold_parser.add_argument('bucket_name')

    args = parser.parse_args()

    if args.command == 'set-retention-policy':
        set_retention_policy(args.bucket_name, args.retention_period)
    elif args.command == 'remove-retention-policy':
        remove_retention_policy(args.bucket_name)
    elif args.command == 'lock-retention-policy':
        lock_retention_policy(args.bucket_name)
    elif args.command == 'get-retention-policy':
        get_retention_policy(args.bucket_name)
    elif args.command == 'set-temporary-hold':
        set_temporary_hold(args.bucket_name, args.blob_name)
    elif args.command == 'release-temporary-hold':
        release_temporary_hold(args.bucket_name, args.blob_name)
    elif args.command == 'set-event-based-hold':
        set_event_based_hold(args.bucket_name, args.blob_name)
    elif args.command == 'release-event-based-hold':
        release_event_based_hold(args.bucket_name, args.blob_name)
    elif args.command == 'enable-default-event-based-hold':
        enable_default_event_based_hold(args.bucket_name)
    elif args.command == 'disable-default-event-based-hold':
        disable_default_event_based_hold(args.bucket_name)
    elif args.command == 'get-default-event-based-hold':
        get_default_event_based_hold(args.bucket_name)
