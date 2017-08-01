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
import datetime
import pprint

from google.cloud import storage


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


def get_bucket_labels(bucket_name):
    """Prints out a bucket's labels."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    labels = bucket.labels
    pprint.pprint(labels)


def add_bucket_label(bucket_name):
    """Add a label to a bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    labels = bucket.labels
    labels['example'] = 'label'
    bucket.labels = labels
    bucket.patch()

    print('Updated labels on {}.'.format(bucket.name))
    pprint.pprint(bucket.labels)


def remove_bucket_label(bucket_name):
    """Remove a label from a bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    labels = bucket.labels

    if 'example' in labels:
        del labels['example']

    bucket.labels = labels
    bucket.patch()

    print('Updated labels on {}.'.format(bucket.name))
    pprint.pprint(bucket.labels)


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


def blob_metadata(bucket_name, blob_name):
    """Prints out a blob's metadata."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(blob_name)

    print('Blob: {}'.format(blob.name))
    print('Bucket: {}'.format(blob.bucket.name))
    print('Storage class: {}'.format(blob.storage_class))
    print('ID: {}'.format(blob.id))
    print('Size: {} bytes'.format(blob.size))
    print('Updated: {}'.format(blob.updated))
    print('Generation: {}'.format(blob.generation))
    print('Metageneration: {}'.format(blob.metageneration))
    print('Etag: {}'.format(blob.etag))
    print('Owner: {}'.format(blob.owner))
    print('Component count: {}'.format(blob.component_count))
    print('Crc32c: {}'.format(blob.crc32c))
    print('md5_hash: {}'.format(blob.md5_hash))
    print('Cache-control: {}'.format(blob.cache_control))
    print('Content-type: {}'.format(blob.content_type))
    print('Content-disposition: {}'.format(blob.content_disposition))
    print('Content-encoding: {}'.format(blob.content_encoding))
    print('Content-language: {}'.format(blob.content_language))
    print('Metadata: {}'.format(blob.metadata))


def make_blob_public(bucket_name, blob_name):
    """Makes a blob publicly accessible."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.make_public()

    print('Blob {} is publicly accessible at {}'.format(
        blob.name, blob.public_url))


def generate_signed_url(bucket_name, blob_name):
    """Generates a signed URL for a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        # This URL is valid for 1 hour
        expiration=datetime.timedelta(hours=1),
        # Allow GET requests using this URL.
        method='GET')

    print('The signed url for {} is {}'.format(blob.name, url))


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
    subparsers.add_parser('get-bucket-labels', help=get_bucket_labels.__doc__)
    subparsers.add_parser('add-bucket-label', help=add_bucket_label.__doc__)
    subparsers.add_parser(
        'remove-bucket-label', help=remove_bucket_label.__doc__)
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

    metadata_parser = subparsers.add_parser(
        'metadata', help=blob_metadata.__doc__)
    metadata_parser.add_argument('blob_name')

    make_public_parser = subparsers.add_parser(
        'make-public', help=make_blob_public.__doc__)
    make_public_parser.add_argument('blob_name')

    signed_url_parser = subparsers.add_parser(
        'signed-url', help=generate_signed_url.__doc__)
    signed_url_parser.add_argument('blob_name')

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
    elif args.command == 'delete-bucket':
        delete_bucket(args.bucket_name)
    if args.command == 'get-bucket-labels':
        get_bucket_labels(args.bucket_name)
    if args.command == 'add-bucket-label':
        add_bucket_label(args.bucket_name)
    if args.command == 'remove-bucket-label':
        remove_bucket_label(args.bucket_name)
    elif args.command == 'list':
        list_blobs(args.bucket_name)
    elif args.command == 'list-with-prefix':
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
    elif args.command == 'metadata':
        blob_metadata(args.bucket_name, args.blob_name)
    elif args.command == 'make-public':
        make_blob_public(args.bucket_name, args.blob_name)
    elif args.command == 'signed-url':
        generate_signed_url(args.bucket_name, args.blob_name)
    elif args.command == 'rename':
        rename_blob(args.bucket_name, args.blob_name, args.new_name)
    elif args.command == 'copy':
        copy_blob(
            args.bucket_name,
            args.blob_name,
            args.new_bucket_name,
            args.new_blob_name)
