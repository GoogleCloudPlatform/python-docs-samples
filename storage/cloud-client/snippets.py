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

"""This application demonstrates how to perform basic operations on blobs
(objects) in a Google Cloud Storage bucket.

For more information, see the README.md under /storage  and the documentation
at https://cloud.google.com/storage/docs.
"""

import argparse

from gcloud import storage


def create_bucket(bucket_name):
    """Creates a new bucket."""
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    print('Bucket {} created'.format(bucket.name))


def delete_bucket(bucket_name):
    """Deletes a bucket. The bucket must be empty."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()
    print('Bucket {} deleted'.format(bucket.name))


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    for blob in blobs:
        print(blob.name)


def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    """Lists all the blobs in the bucket that begin with the prefix.

    This can be used to list all blobs in a "folder", e.g. "public/".

    The delimiter argument can be used to restrict the results to only the
    "files" in the given "folder". Without the delimiter, the entire tree under
    the prefix is returned. For example, given these blobs:

        /a/1.txt
        /a/b/2.txt

    If you just specify prefix = '/a', you'll get back:

        /a/1.txt
        /a/b/2.txt

    However, if you specify prefix='/a' and delimiter='/', you'll get back:

        /a/1.txt

    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)

    print('Blobs:')
    for blob in blobs:
        print(blob.name)

    if delimiter:
        print('Prefixes:')
        for prefix in blobs.prefixes:
            print(prefix)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print('Blob {} deleted.'.format(blob_name))


def make_blob_public(bucket_name, blob_name):
    """Makes a blob publicly accessible."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.make_public()

    print('Blob {} is publicly accessible at {}'.format(
        blob.name, blob.public_url))


def rename_blob(bucket_name, blob_name, new_name):
    """Renames a blob."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    new_blob = bucket.rename_blob(blob, new_name)

    print('Blob {} has been renamed to {}'.format(
        blob.name, new_blob.name))


def copy_blob(bucket_name, blob_name, new_bucket_name, new_blob_name):
    """Copies a blob from one bucket to another with a new name."""
    storage_client = storage.Client()
    source_bucket = storage_client.get_bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.get_bucket(new_bucket_name)

    new_blob = source_bucket.copy_blob(
        source_blob, destination_bucket, new_blob_name)

    print('Blob {} in bucket {} copied to blob {} in bucket {}.'.format(
        source_blob.name, source_bucket.name, new_blob.name,
        destination_bucket.name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('bucket_name', help='Your cloud storage bucket.')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('create-bucket', help=create_bucket.__doc__)
    subparsers.add_parser('delete-bucket', help=delete_bucket.__doc__)
    subparsers.add_parser('list', help=list_blobs.__doc__)

    list_with_prefix_parser = subparsers.add_parser(
        'list-with-prefix', help=list_blobs_with_prefix.__doc__)
    list_with_prefix_parser.add_argument('prefix')
    list_with_prefix_parser.add_argument('--delimiter', default=None)

    upload_parser = subparsers.add_parser('upload', help=upload_blob.__doc__)
    upload_parser.add_argument('source_file_name')
    upload_parser.add_argument('destination_blob_name')

    download_parser = subparsers.add_parser(
        'download', help=download_blob.__doc__)
    download_parser.add_argument('source_blob_name')
    download_parser.add_argument('destination_file_name')

    delete_parser = subparsers.add_parser('delete', help=delete_blob.__doc__)
    delete_parser.add_argument('blob_name')

    rename_parser = subparsers.add_parser('rename', help=rename_blob.__doc__)
    rename_parser.add_argument('blob_name')
    rename_parser.add_argument('new_name')

    copy_parser = subparsers.add_parser('copy', help=rename_blob.__doc__)
    copy_parser.add_argument('blob_name')
    copy_parser.add_argument('new_bucket_name')
    copy_parser.add_argument('new_blob_name')

    args = parser.parse_args()

    if args.command == 'create-bucket':
        create_bucket(args.bucket_name)
    if args.command == 'delete-bucket':
        delete_bucket(args.bucket_name)
    if args.command == 'list':
        list_blobs(args.bucket_name)
    if args.command == 'list-with-prefix':
        list_blobs_with_prefix(args.bucket_name, args.prefix, args.delimiter)
    elif args.command == 'upload':
        upload_blob(
            args.bucket_name,
            args.source_file_name,
            args.destination_blob_name)
    elif args.command == 'download':
        download_blob(
            args.bucket_name,
            args.source_blob_name,
            args.destination_file_name)
    elif args.command == 'delete':
        delete_blob(args.bucket_name, args.blob_name)
    elif args.command == 'rename':
        rename_blob(args.bucket_name, args.blob_name, args.new_name)
    elif args.command == 'copy':
        copy_blob(
            args.bucket_name,
            args.blob_name,
            args.new_bucket_name,
            args.new_blob_name)
