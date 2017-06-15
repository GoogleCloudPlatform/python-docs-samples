# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Demonstrates how to authenticate to Google Cloud Platform APIs using
the Google API Client."""

import argparse


def implicit(project):
    import googleapiclient.discovery

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = googleapiclient.discovery.build('storage', 'v1')

    # Make an authenticated API request
    buckets = storage_client.buckets().list(project=project).execute()
    print(buckets)


def explicit(project):
    from google.oauth2 import service_account
    import googleapiclient.discovery

    # Construct service account credentials using the service account key
    # file.
    credentials = service_account.Credentials.from_service_account_file(
        'service_account.json')

    # Explicitly pass the credentials to the client library.
    storage_client = googleapiclient.discovery.build(
        'storage', 'v1', credentials=credentials)

    # Make an authenticated API request
    buckets = storage_client.buckets().list(project=project).execute()
    print(buckets)


def explicit_compute_engine(project):
    from google.auth import compute_engine
    import googleapiclient.discovery

    # Explicitly use Compute Engine credentials. These credentials are
    # available on Compute Engine, App Engine Flexible, and Container Engine.
    credentials = compute_engine.Credentials()

    # Explicitly pass the credentials to the client library.
    storage_client = googleapiclient.discovery.build(
        'storage', 'v1', credentials=credentials)

    # Make an authenticated API request
    buckets = storage_client.buckets().list(project=project).execute()
    print(buckets)


def explicit_app_engine(project):
    from google.auth import app_engine
    import googleapiclient.discovery

    # Explicitly use App Engine credentials. These credentials are
    # only available when running on App Engine Standard.
    credentials = app_engine.Credentials()

    # Explicitly pass the credentials to the client library.
    storage_client = googleapiclient.discovery.build(
        'storage', 'v1', credentials=credentials)

    # Make an authenticated API request
    buckets = storage_client.buckets().list(project=project).execute()
    print(buckets)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('implicit', help=implicit.__doc__)
    subparsers.add_parser('explicit', help=explicit.__doc__)
    subparsers.add_parser(
        'explicit_compute_engine', help=explicit_compute_engine.__doc__)
    subparsers.add_parser(
        'explicit_app_engine', help=explicit_app_engine.__doc__)

    args = parser.parse_args()

    if args.command == 'implicit':
        implicit(args.project)
    elif args.command == 'explicit':
        explicit(args.project)
    elif args.command == 'explicit_compute_engine':
        explicit_compute_engine(args.project)
    elif args.command == 'explicit_app_engine':
        explicit_app_engine(args.project)
