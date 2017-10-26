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

For more information, see the README.rst.

Example invocation:
    $ python snippets.py list-datasets

The dataset and table should already exist.
"""

import argparse

from google.cloud import bigquery


def list_projects():
    bigquery_client = bigquery.Client()

    for project in bigquery_client.list_projects():
        print(project.project_id)


def list_datasets(project=None):
    """Lists all datasets in a given project.

    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)

    for dataset in bigquery_client.list_datasets():
        print(dataset.dataset_id)


def create_dataset(dataset_id, project=None):
    """Craetes a dataset in a given project.

    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)

    dataset_ref = bigquery_client.dataset(dataset_id)

    dataset = bigquery_client.create_dataset(bigquery.Dataset(dataset_ref))

    print('Created dataset {}.'.format(dataset.dataset_id))


def list_tables(dataset_id, project=None):
    """Lists all of the tables in a given dataset.

    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)
    dataset_ref = bigquery_client.dataset(dataset_id)

    for table in bigquery_client.list_dataset_tables(dataset_ref):
        print(table.table_id)


def create_table(dataset_id, table_id, project=None):
    """Creates a simple table in the given dataset.

    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)
    dataset_ref = bigquery_client.dataset(dataset_id)

    table_ref = dataset_ref.table(table_id)
    table = bigquery.Table(table_ref)

    # Set the table schema
    table.schema = (
        bigquery.SchemaField('Name', 'STRING'),
        bigquery.SchemaField('Age', 'INTEGER'),
        bigquery.SchemaField('Weight', 'FLOAT'),
    )

    table = bigquery_client.create_table(table)

    print('Created table {} in dataset {}.'.format(table_id, dataset_id))


def list_rows(dataset_id, table_id, project=None):
    """Prints rows in the given table.

    Will print 25 rows at most for brevity as tables can contain large amounts
    of rows.

    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    # Get the table from the API so that the schema is available.
    table = bigquery_client.get_table(table_ref)

    # Load at most 25 results.
    rows = bigquery_client.list_rows(table, max_results=25)

    # Use format to create a simple table.
    format_string = '{!s:<16} ' * len(table.schema)

    # Print schema field names
    field_names = [field.name for field in table.schema]
    print(format_string.format(*field_names))

    for row in rows:
        print(format_string.format(*row))


def copy_table(dataset_id, table_id, new_table_id, project=None):
    """Copies a table.

    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    # This sample shows the destination table in the same dataset and project,
    # however, it's possible to copy across datasets and projects. You can
    # also copy multiple source tables into a single destination table by
    # providing addtional arguments to `copy_table`.
    destination_table_ref = dataset_ref.table(new_table_id)

    # Create a job to copy the table to the destination table.
    # Start by creating a job configuration
    job_config = bigquery.CopyJobConfig()

    # Configure the job to create the table if it doesn't exist.
    job_config.create_disposition = (
        bigquery.job.CreateDisposition.CREATE_IF_NEEDED)

    copy_job = bigquery_client.copy_table(
        table_ref, destination_table_ref, job_config=job_config)

    print('Waiting for job to finish...')
    copy_job.result()

    print('Table {} copied to {}.'.format(table_id, new_table_id))


def delete_table(dataset_id, table_id, project=None):
    """Deletes a table in a given dataset.

    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    bigquery_client.delete_table(table_ref)

    print('Table {}:{} deleted.'.format(dataset_id, table_id))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--project', default=None)

    subparsers = parser.add_subparsers(dest='command')

    list_projects_parser = subparsers.add_parser(
        'list-projects', help=list_projects.__doc__)

    list_datasets_parser = subparsers.add_parser(
        'list-datasets', help=list_datasets.__doc__)

    create_dataset_parser = subparsers.add_parser(
        'list-datasets', help=list_datasets.__doc__)
    create_dataset_parser.add_argument('dataset_id')

    list_tables_parser = subparsers.add_parser(
        'list-tables', help=list_tables.__doc__)
    list_tables_parser.add_argument('dataset_id')

    create_table_parser = subparsers.add_parser(
        'create-table', help=create_table.__doc__)
    create_table_parser.add_argument('dataset_id')
    create_table_parser.add_argument('table_id')

    list_rows_parser = subparsers.add_parser(
        'list-rows', help=list_rows.__doc__)
    list_rows_parser.add_argument('dataset_id')
    list_rows_parser.add_argument('table_id')

    copy_table_parser = subparsers.add_parser(
        'copy-table', help=copy_table.__doc__)
    copy_table_parser.add_argument('dataset_id')
    copy_table_parser.add_argument('table_id')
    copy_table_parser.add_argument('new_table_id')

    delete_table_parser = subparsers.add_parser(
        'delete-table', help=delete_table.__doc__)
    delete_table_parser.add_argument('dataset_id')
    delete_table_parser.add_argument('table_id')

    args = parser.parse_args()

    if args.command == 'list-projects':
        list_projects()
    elif args.command == 'list-datasets':
        list_datasets(args.project)
    elif args.command == 'create-dataset':
        create_dataset(args.dataset_id, args.project)
    elif args.command == 'list-tables':
        list_tables(args.dataset_id, args.project)
    elif args.command == 'create-table':
        create_table(args.dataset_id, args.table_id, args.project)
    elif args.command == 'list-rows':
        list_rows(args.dataset_id, args.table_id, args.project)
    elif args.command == 'copy-table':
        copy_table(args.dataset_id, args.table_id, args.new_table_id)
    elif args.command == 'delete-table':
        delete_table(args.dataset_id, args.table_id, args.project)
