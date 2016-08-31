#!/usr/bin/env python

# Copyright 2016 Google, Inc.
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

"""This application demonstrates how to manage access control lists (acls) in
Google Cloud Storage.

For more information, see the README.md under /storage and the documentation
at https://cloud.google.com/storage/docs/encryption.
"""

import argparse

from gcloud import storage


def get_bucket_acl(bucket_name):
    """Prints out a bucket's access control list."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for entry in bucket.acl:
        print('{}: {}'.format(entry['role'], entry['entity']))


def get_bucket_acl_for_user(bucket_name, user_email):
    """Prints out a bucket's access control list for a given user."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    bucket.acl.reload()

    # You can also use `group`, `domain`, `all_authenticated` and `all` to
    # get the roles for different types of entities.
    roles = bucket.acl.user(user_email).get_roles()

    print(roles)


def set_bucket_acl(bucket_name, user_email):
    """Adds a user as an owner on the given bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # You can also use `group`, `domain`, `all_authenticated` and `all` to
    # grant access to different types of entities. You can also use
    # `grant_read` or `grant_write` to grant different roles.
    bucket.acl.user(user_email).grant_owner()
    bucket.acl.save()

    print('Added user {} as an owner on bucket {}.'.format(
        user_email, bucket_name))


def remove_bucket_acl(bucket_name, user_email):
    """Removes a user from the access control list of the given bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # You can also use `group`, `domain`, `all_authenticated` and `all` to
    # remove access for different types of entities.
    bucket.acl.user(user_email).revoke_read()
    bucket.acl.user(user_email).revoke_write()
    bucket.acl.user(user_email).revoke_owner()
    bucket.acl.save()

    print('Removed user {} from bucket {}.'.format(
        user_email, bucket_name))


def set_bucket_default_acl(bucket_name, user_email):
    """Adds a user as an owner in the given bucket's default object access
    control list."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # You can also use `group`, `domain`, `all_authenticated` and `all` to
    # grant access to different types of entities. You can also use
    # `grant_read` or `grant_write` to grant different roles.
    bucket.default_object_acl.user(user_email).grant_owner()
    bucket.default_object_acl.save()

    print('Added user {} as an owner in the default acl on bucket {}.'.format(
        user_email, bucket_name))


def remove_bucket_default_acl(bucket_name, user_email):
    """Removes a user from the access control list of the given bucket's
    default object access control list."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # You can also use `group`, `domain`, `all_authenticated` and `all` to
    # remove access for different types of entities.
    bucket.default_object_acl.user(user_email).revoke_read()
    bucket.default_object_acl.user(user_email).revoke_write()
    bucket.default_object_acl.user(user_email).revoke_owner()
    bucket.default_object_acl.save()

    print('Removed user {} from the default acl of bucket {}.'.format(
        user_email, bucket_name))


def get_blob_acl(bucket_name, blob_name):
    """Prints out a blob's access control list."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    for entry in blob.acl:
        print('{}: {}'.format(entry['role'], entry['entity']))


def get_blob_acl_for_user(bucket_name, blob_name, user_email):
    """Prints out a bucket's access control list for a given user."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.acl.reload()

    # You can also use `group`, `domain`, `all_authenticated` and `all` to
    # get the roles for different types of entities.
    roles = blob.acl.user(user_email).get_roles()

    print(roles)


def set_blob_acl(bucket_name, blob_name, user_email):
    """Adds a user as an owner on the given blob."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # You can also use `group`, `domain`, `all_authenticated` and `all` to
    # grant access to different types of entities. You can also use
    # `grant_read` or `grant_write` to grant different roles.
    blob.acl.user(user_email).grant_owner()
    blob.acl.save()

    print('Added user {} as an owner on blob {} in bucket {}.'.format(
        user_email, blob_name, bucket_name))


def remove_blob_acl(bucket_name, blob_name, user_email):
    """Removes a user from the access control list of the given blob in the
    given bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # You can also use `group`, `domain`, `all_authenticated` and `all` to
    # remove access for different types of entities.
    blob.acl.user(user_email).revoke_read()
    blob.acl.user(user_email).revoke_write()
    blob.acl.user(user_email).revoke_owner()
    blob.acl.save()

    print('Removed user {} from blob {} in bucket {}.'.format(
        user_email, blob_name, bucket_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    get_bucket_acl_parser = subparsers.add_parser(
        'get-bucket-acl', help=get_bucket_acl.__doc__)
    get_bucket_acl_parser.add_argument('bucket_name')

    get_bucket_acl_for_user_parser = subparsers.add_parser(
        'get-bucket-acl-for-user', help=get_bucket_acl.__doc__)
    get_bucket_acl_for_user_parser.add_argument('bucket_name')
    get_bucket_acl_for_user_parser.add_argument('user_email')

    set_bucket_acl_parser = subparsers.add_parser(
        'set-bucket-acl', help=set_bucket_acl.__doc__)
    set_bucket_acl_parser.add_argument('bucket_name')
    set_bucket_acl_parser.add_argument('user_email')

    remove_bucket_acl_parser = subparsers.add_parser(
        'remove-bucket-acl', help=remove_bucket_acl.__doc__)
    remove_bucket_acl_parser.add_argument('bucket_name')
    remove_bucket_acl_parser.add_argument('user_email')

    set_bucket_default_acl_parser = subparsers.add_parser(
        'set-bucket-default-acl', help=set_bucket_default_acl.__doc__)
    set_bucket_default_acl_parser.add_argument('bucket_name')
    set_bucket_default_acl_parser.add_argument('user_email')

    remove_bucket_default_acl_parser = subparsers.add_parser(
        'remove-bucket-default-acl', help=remove_bucket_default_acl.__doc__)
    remove_bucket_default_acl_parser.add_argument('bucket_name')
    remove_bucket_default_acl_parser.add_argument('user_email')

    get_blob_acl_parser = subparsers.add_parser(
        'get-blob-acl', help=get_blob_acl.__doc__)
    get_blob_acl_parser.add_argument('bucket_name')
    get_blob_acl_parser.add_argument('blob_name')

    get_blob_acl_for_user_parser = subparsers.add_parser(
        'get-blob-acl-for-user', help=get_blob_acl_for_user.__doc__)
    get_blob_acl_for_user_parser.add_argument('bucket_name')
    get_blob_acl_for_user_parser.add_argument('blob_name')
    get_blob_acl_for_user_parser.add_argument('user_email')

    set_blob_acl_parser = subparsers.add_parser(
        'set-blob-acl', help=set_blob_acl.__doc__)
    set_blob_acl_parser.add_argument('bucket_name')
    set_blob_acl_parser.add_argument('blob_name')
    set_blob_acl_parser.add_argument('user_email')

    remove_blob_acl_parser = subparsers.add_parser(
        'remove-blob-acl', help=remove_blob_acl.__doc__)
    remove_blob_acl_parser.add_argument('bucket_name')
    remove_blob_acl_parser.add_argument('blob_name')
    remove_blob_acl_parser.add_argument('user_email')

    args = parser.parse_args()

    if args.command == 'get-bucket-acl':
        get_bucket_acl(args.bucket_name)
    elif args.command == 'get-bucket-acl-for-user':
        get_bucket_acl_for_user(args.bucket_name, args.user_email)
    elif args.command == 'set-bucket-acl':
        set_bucket_acl(args.bucket_name, args.user_email)
    elif args.command == 'remove-bucket-acl':
        remove_bucket_acl(args.bucket_name, args.user_email)
    elif args.command == 'set-bucket-default-acl':
        set_bucket_default_acl(args.bucket_name, args.user_email)
    elif args.command == 'remove-bucket-default-acl':
        remove_bucket_default_acl(args.bucket_name, args.user_email)
    elif args.command == 'get-blob-acl':
        get_blob_acl(args.bucket_name, args.blob_name)
    elif args.command == 'get-blob-acl-for-user':
        get_blob_acl_for_user(
            args.bucket_name, args.blob_name, args.user_email)
    elif args.command == 'set-blob-acl':
        set_blob_acl(args.bucket_name, args.blob_name, args.user_email)
    elif args.command == 'remove-blob-acl':
        remove_blob_acl(args.bucket_name, args.blob_name, args.user_email)
