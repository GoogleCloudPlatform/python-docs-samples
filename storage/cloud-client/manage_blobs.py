#!/usr/bin/env python

# Copyright (C) 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command-line sample application for simple CRUD management of blobs in a
given bucket.

For more information, see the README.md under /storage.
"""

import argparse

from gcloud import storage


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    for blob in blobs:
        print(blob.name)


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bucket_name', help='Your cloud storage bucket.')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('list', help=list_blobs.__doc__)

    upload_parser = subparsers.add_parser('upload', help=upload_blob.__doc__)
    upload_parser.add_argument('source_file_name')
    upload_parser.add_argument('destination_blob_name')

    download_parser = subparsers.add_parser(
        'download', help=download_blob.__doc__)
    download_parser.add_argument('source_blob_name')
    download_parser.add_argument('destination_file_name')

    delete_parser = subparsers.add_parser('delete', help=delete_blob.__doc__)
    delete_parser.add_argument('blob_name')

    args = parser.parse_args()

    if args.command == 'list':
        list_blobs(args.bucket_name)
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
