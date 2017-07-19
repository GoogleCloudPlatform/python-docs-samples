# Copyright 2017 Google Inc.
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

"""Demonstrates how to authenticate to Google BigQuery using the Google Cloud
Client Libraries."""

import argparse


def implicit():
    from google.cloud import bigquery

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    bigquery_client = bigquery.Client()

    # Make an authenticated API request
    datasets = list(bigquery_client.list_datasets())
    print(datasets)


def explicit():
    from google.cloud import bigquery

    # Explicitly use service account credentials by specifying the private key
    # file. All clients in google-cloud-python have this helper, see
    # https://google-cloud-python.readthedocs.io/en/latest/core/modules.html
    #   #google.cloud.client.Client.from_service_account_json
    bigquery_client = bigquery.Client.from_service_account_json(
        'service_account.json')

    # Make an authenticated API request
    buckets = list(bigquery_client.list_datasets())
    print(buckets)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('implicit', help=implicit.__doc__)
    subparsers.add_parser('explicit', help=explicit.__doc__)

    args = parser.parse_args()

    if args.command == 'implicit':
        implicit()
    elif args.command == 'explicit':
        explicit()
