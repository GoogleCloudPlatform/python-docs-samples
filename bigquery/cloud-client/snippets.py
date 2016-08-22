#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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

"""Samples that demonstrate basic operations in the BigQuery API.

For more information, see the README.md under /bigquery.

Example invocation:
    $ python snippets.py list-datasets

The dataset and table should already exist.
"""

import argparse

from gcloud import bigquery


def list_projects():
    raise NotImplementedError(
        'https://github.com/GoogleCloudPlatform/gcloud-python/issues/2143')


def list_datasets(project=None):
    """Lists all datasets in a given project.

    If no project is specified, then the currently active project is used
    """
    bigquery_client = bigquery.Client(project=project)

    datasets = []
    page_token = None

    while True:
        results, page_token = bigquery_client.list_datasets(
            page_token=page_token)
        datasets.extend(results)

        if not page_token:
            break

    for dataset in datasets:
        print(dataset.name)


def list_tables(dataset_name, project=None):
    """Lists all of the tables in a given dataset.

    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)
    dataset = bigquery_client.dataset(dataset_name)

    if not dataset.exists():
        print('Dataset {} does not exist.'.format(dataset_name))
        return

    tables = []
    page_token = None

    while True:
        results, page_token = dataset.list_tables(page_token=page_token)
        tables.extend(results)

        if not page_token:
            break

    for table in tables:
        print(table.name)


def list_rows(dataset_name, table_name, project=None):
    """Prints rows in the given table.

    Will print 25 rows at most for brevity as tables can contain large amounts
    of rows.

    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)
    dataset = bigquery_client.dataset(dataset_name)
    table = dataset.table(table_name)

    if not table.exists():
        print('Table {}:{} does not exist.'.format(dataset_name, table_name))
        return

    # Reload the table so that the schema is available.
    table.reload()

    rows = []
    page_token = None

    # Load at most 25 results. You can change this to `while True` and change
    # the max_results argument to load more rows from BigQuery, but note
    # that this can take some time. It's preferred to use a query.
    while len(rows) < 25:
        results, total_rows, page_token = table.fetch_data(
            max_results=25, page_token=page_token)
        rows.extend(results)

        if not page_token:
            break

    # Use format to create a simple table.
    format_string = '{:<16} ' * len(table.schema)

    # Print schema field names
    field_names = [field.name for field in table.schema]
    print(format_string.format(*field_names))

    for row in rows:
        print(format_string.format(*row))


def delete_table(dataset_name, table_name, project=None):
    """Deletes a table in a given dataset.

    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)
    dataset = bigquery_client.dataset(dataset_name)
    table = dataset.table(table_name)

    table.delete()

    print('Table {}:{} deleted.'.format(dataset_name, table_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--project', default=None)

    subparsers = parser.add_subparsers(dest='command')

    list_datasets_parser = subparsers.add_parser(
        'list-datasets', help=list_datasets.__doc__)

    list_tables_parser = subparsers.add_parser(
        'list-tables', help=list_tables.__doc__)
    list_tables_parser.add_argument('dataset_name')

    list_rows_parser = subparsers.add_parser(
        'list-rows', help=list_rows.__doc__)
    list_rows_parser.add_argument('dataset_name')
    list_rows_parser.add_argument('table_name')

    delete_table_parser = subparsers.add_parser(
        'delete-table', help=delete_table.__doc__)
    delete_table_parser.add_argument('dataset_name')
    delete_table_parser.add_argument('table_name')

    args = parser.parse_args()

    if args.command == 'list-datasets':
        list_datasets(args.project)
    elif args.command == 'list-tables':
        list_tables(args.dataset_name, args.project)
    elif args.command == 'list-rows':
        list_rows(args.dataset_name, args.table_name, args.project)
    elif args.command == 'delete-table':
        delete_table(args.dataset_name, args.table_name, args.project)
