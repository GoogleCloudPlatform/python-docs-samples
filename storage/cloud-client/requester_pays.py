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

"""This application demonstrates how to use requester pays features on Google
Cloud Storage buckets.

For more information, see the documentation at
https://cloud.google.com/storage/docs/using-requester-pays.
"""

import argparse

from google.cloud import storage


def get_requester_pays_status(bucket_name):
    """Get a bucket's requester pays metadata"""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    requester_pays_status = bucket.requester_pays
    if requester_pays_status:
        print('Requester Pays is enabled for {}'.format(bucket_name))
    else:
        print('Requester Pays is disabled for {}'.format(bucket_name))


def enable_requester_pays(bucket_name):
    """Enable a bucket's requesterpays metadata"""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    bucket.requester_pays = True
    bucket.patch()
    print('Requester Pays has been enabled for {}'.format(bucket_name))


def disable_requester_pays(bucket_name):
    """Disable a bucket's requesterpays metadata"""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    bucket.requester_pays = False
    bucket.patch()
    print('Requester Pays has been disabled for {}'.format(bucket_name))


def download_file_requester_pays(
        bucket_name, project_id, source_blob_name, destination_file_name):
    """Download file using specified project as the requester"""
    storage_client = storage.Client()
    user_project = project_id
    bucket = storage_client.bucket(bucket_name, user_project)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {} using a requester-pays request.'.format(
        source_blob_name,
        destination_file_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('bucket_name', help='Your Cloud Storage bucket name.')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser(
        'check-status', help=get_requester_pays_status.__doc__)

    subparsers.add_parser(
        'enable', help=enable_requester_pays.__doc__)

    subparsers.add_parser(
        'disable', help=disable_requester_pays.__doc__)

    download_parser = subparsers.add_parser(
        'download', help=download_file_requester_pays.__doc__)
    download_parser.add_argument('project')
    download_parser.add_argument('source_blob_name')
    download_parser.add_argument('destination_file_name')

    args = parser.parse_args()

    if args.command == 'check-status':
        get_requester_pays_status(args.bucket_name)
    elif args.command == 'enable':
        enable_requester_pays(args.bucket_name)
    elif args.command == 'disable':
        disable_requester_pays(args.bucket_name)
    elif args.command == 'download':
        download_file_requester_pays(
            args.bucket_name, args.project, args.source_blob_name,
            args.destination_file_name)
