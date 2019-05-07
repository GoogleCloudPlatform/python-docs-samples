#!/usr/bin/env python

# Copyright 2019 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
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

"""This application demonstrates how to perform basic operations on entries
with the Cloud Data Catalog API.

For more information, see the README.md under /datacatalog and the documentation
at https://cloud.google.com/data-catalog/docs.
"""

import argparse


def lookup_bigquery_dataset(project_id, dataset_id):
    """Retrieves Data Catalog's entry for the given dataset."""
    from google.cloud import datacatalog_v1beta1

    datacatalog = datacatalog_v1beta1.DataCatalogClient()

    resource_name = '//bigquery.googleapis.com/projects/{}/datasets/{}'\
        .format(project_id, dataset_id)

    return datacatalog.lookup_entry(linked_resource=resource_name)


def lookup_bigquery_table(project_id, dataset_id, table_id):
    """Retrieves Data Catalog's entry for the given table."""
    from google.cloud import datacatalog_v1beta1

    datacatalog = datacatalog_v1beta1.DataCatalogClient()

    resource_name = '//bigquery.googleapis.com/projects/{}/datasets/{}/tables/{}'\
        .format(project_id, dataset_id, table_id)

    return datacatalog.lookup_entry(linked_resource=resource_name)


def lookup_pubsub_topic(project_id, topic_id):
    """Retrieves Data Catalog's entry for the given topic."""
    from google.cloud import datacatalog_v1beta1

    datacatalog = datacatalog_v1beta1.DataCatalogClient()

    resource_name = '//pubsub.googleapis.com/projects/{}/topics/{}'\
        .format(project_id, topic_id)

    return datacatalog.lookup_entry(linked_resource=resource_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('project_id', help='Your Google Cloud project ID')

    subparsers = parser.add_subparsers(dest='command')

    bigquery_dataset_parser = subparsers.add_parser(
        'lookup-bigquery-dataset', help=lookup_bigquery_dataset.__doc__)
    bigquery_dataset_parser.add_argument('dataset_id')

    bigquery_table_parser = subparsers.add_parser(
        'lookup-bigquery-table', help=lookup_bigquery_table.__doc__)
    bigquery_table_parser.add_argument('dataset_id')
    bigquery_table_parser.add_argument('table_id')

    pubsub_topic_parser = subparsers.add_parser(
        'lookup-pubsub-topic', help=lookup_pubsub_topic.__doc__)
    pubsub_topic_parser.add_argument('topic_id')

    args = parser.parse_args()

    if args.command == 'lookup-bigquery-dataset':
        lookup_bigquery_dataset(args.project_id, args.dataset_id)
    elif args.command == 'lookup-bigquery-table':
        lookup_bigquery_table(args.project_id, args.dataset_id, args.table_id)
    elif args.command == 'lookup-pubsub-topic':
        lookup_pubsub_topic(args.project_id, args.topic_id)
