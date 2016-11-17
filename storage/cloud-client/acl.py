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

from google.cloud import storage


def print_bucket_acl(bucket_name):
    """Prints out a bucket's access control list."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for entry in bucket.acl:
        print('{}: {}'.format(entry['role'], entry['entity']))


def print_bucket_acl_for_user(bucket_name, user_email):
    """Prints out a bucket's access control list for a given user."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Reload fetches the current ACL from Cloud Storage.
    bucket.acl.reload()

    # You can also use `group`, `domain`, `all_authenticated` and `all` to
    # get the roles for different types of entities.
    roles = bucket.acl.user(user_email).get_roles()

    print(roles)


def add_bucket_owner(bucket_name, user_email):
    """Adds a user as an owner on the given bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Reload fetches the current ACL from Cloud Storage.
    bucket.acl.reload()

    # You can also use `group()`, `domain()`, `all_authenticated()` and `all()`
    # to grant access to different types of entities.
    # You can also use `grant_read()` or `grant_write()` to grant different
    # roles.
    bucket.acl.user(user_email).grant_owner()
    bucket.acl.save()

    print('Added user {} as an owner on bucket {}.'.format(
        user_email, bucket_name))


def remove_bucket_owner(bucket_name, user_email):
    """Removes a user from the access control list of the given bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Reload fetches the current ACL from Cloud Storage.
    bucket.acl.reload()

    # You can also use `group`, `domain`, `all_authenticated` and `all` to
    # remove access for different types of entities.
    bucket.acl.user(user_email).revoke_read()
    bucket.acl.user(user_email).revoke_write()
    bucket.acl.user(user_email).revoke_owner()
    bucket.acl.save()

    print('Removed user {} from bucket {}.'.format(
        user_email, bucket_name))


def add_bucket_default_owner(bucket_name, user_email):
    """Adds a user as an owner in the given bucket's default object access
    control list."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Reload fetches the current ACL from Cloud Storage.
    bucket.acl.reload()

    # You can also use `group`, `domain`, `all_authenticated` and `all` to
    # grant access to different types of entities. You can also use
    # `grant_read` or `grant_write` to grant different roles.
    bucket.default_object_acl.user(user_email).grant_owner()
    bucket.default_object_acl.save()

    print('Added user {} as an owner in the default acl on bucket {}.'.format(
        user_email, bucket_name))


def remove_bucket_default_owner(bucket_name, user_email):
    """Removes a user from the access control list of the given bucket's
    default object access control list."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Reload fetches the current ACL from Cloud Storage.
    bucket.acl.reload()

    # You can also use `group`, `domain`, `all_authenticated` and `all` to
    # remove access for different types of entities.
    bucket.default_object_acl.user(user_email).revoke_read()
    bucket.default_object_acl.user(user_email).revoke_write()
    bucket.default_object_acl.user(user_email).revoke_owner()
    bucket.default_object_acl.save()

    print('Removed user {} from the default acl of bucket {}.'.format(
        user_email, bucket_name))


def print_blob_acl(bucket_name, blob_name):
    """Prints out a blob's access control list."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    for entry in blob.acl:
        print('{}: {}'.format(entry['role'], entry['entity']))


def print_blob_acl_for_user(bucket_name, blob_name, user_email):
    """Prints out a blob's access control list for a given user."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Reload fetches the current ACL from Cloud Storage.
    blob.acl.reload()

    # You can also use `group`, `domain`, `all_authenticated` and `all` to
    # get the roles for different types of entities.
    roles = blob.acl.user(user_email).get_roles()

    print(roles)


def add_blob_owner(bucket_name, blob_name, user_email):
    """Adds a user as an owner on the given blob."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Reload fetches the current ACL from Cloud Storage.
    blob.acl.reload()

    # You can also use `group`, `domain`, `all_authenticated` and `all` to
    # grant access to different types of entities. You can also use
    # `grant_read` or `grant_write` to grant different roles.
    blob.acl.user(user_email).grant_owner()
    blob.acl.save()

    print('Added user {} as an owner on blob {} in bucket {}.'.format(
        user_email, blob_name, bucket_name))


def remove_blob_owner(bucket_name, blob_name, user_email):
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

    print_bucket_acl_parser = subparsers.add_parser(
        'print-bucket-acl', help=print_bucket_acl.__doc__)
    print_bucket_acl_parser.add_argument('bucket_name')

    print_bucket_acl_for_user_parser = subparsers.add_parser(
        'print-bucket-acl-for-user', help=print_bucket_acl.__doc__)
    print_bucket_acl_for_user_parser.add_argument('bucket_name')
    print_bucket_acl_for_user_parser.add_argument('user_email')

    add_bucket_owner_parser = subparsers.add_parser(
        'add-bucket-owner', help=add_bucket_owner.__doc__)
    add_bucket_owner_parser.add_argument('bucket_name')
    add_bucket_owner_parser.add_argument('user_email')

    remove_bucket_owner_parser = subparsers.add_parser(
        'remove-bucket-owner', help=remove_bucket_owner.__doc__)
    remove_bucket_owner_parser.add_argument('bucket_name')
    remove_bucket_owner_parser.add_argument('user_email')

    add_bucket_default_owner_parser = subparsers.add_parser(
        'add-bucket-default-owner', help=add_bucket_default_owner.__doc__)
    add_bucket_default_owner_parser.add_argument('bucket_name')
    add_bucket_default_owner_parser.add_argument('user_email')

    remove_bucket_default_owner_parser = subparsers.add_parser(
        'remove-bucket-default-owner',
        help=remove_bucket_default_owner.__doc__)
    remove_bucket_default_owner_parser.add_argument('bucket_name')
    remove_bucket_default_owner_parser.add_argument('user_email')

    print_blob_acl_parser = subparsers.add_parser(
        'print-blob-acl', help=print_blob_acl.__doc__)
    print_blob_acl_parser.add_argument('bucket_name')
    print_blob_acl_parser.add_argument('blob_name')

    print_blob_acl_for_user_parser = subparsers.add_parser(
        'print-blob-acl-for-user', help=print_blob_acl_for_user.__doc__)
    print_blob_acl_for_user_parser.add_argument('bucket_name')
    print_blob_acl_for_user_parser.add_argument('blob_name')
    print_blob_acl_for_user_parser.add_argument('user_email')

    add_blob_owner_parser = subparsers.add_parser(
        'add-blob-owner', help=add_blob_owner.__doc__)
    add_blob_owner_parser.add_argument('bucket_name')
    add_blob_owner_parser.add_argument('blob_name')
    add_blob_owner_parser.add_argument('user_email')

    remove_blob_owner_parser = subparsers.add_parser(
        'remove-blob-owner', help=remove_blob_owner.__doc__)
    remove_blob_owner_parser.add_argument('bucket_name')
    remove_blob_owner_parser.add_argument('blob_name')
    remove_blob_owner_parser.add_argument('user_email')

    args = parser.parse_args()

    if args.command == 'print-bucket-acl':
        print_bucket_acl(args.bucket_name)
    elif args.command == 'print-bucket-acl-for-user':
        print_bucket_acl_for_user(args.bucket_name, args.user_email)
    elif args.command == 'add-bucket-owner':
        add_bucket_owner(args.bucket_name, args.user_email)
    elif args.command == 'remove-bucket-owner':
        remove_bucket_owner(args.bucket_name, args.user_email)
    elif args.command == 'add-bucket-default-owner':
        add_bucket_default_owner(args.bucket_name, args.user_email)
    elif args.command == 'remove-bucket-default-owner':
        remove_bucket_default_owner(args.bucket_name, args.user_email)
    elif args.command == 'print-blob-acl':
        print_blob_acl(args.bucket_name, args.blob_name)
    elif args.command == 'print-blob-acl-for-user':
        print_blob_acl_for_user(
            args.bucket_name, args.blob_name, args.user_email)
    elif args.command == 'add-blob-owner':
        add_blob_owner(args.bucket_name, args.blob_name, args.user_email)
    elif args.command == 'remove-blob-owner':
        remove_blob_owner(args.bucket_name, args.blob_name, args.user_email)
