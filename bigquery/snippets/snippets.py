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
import time
import uuid

from google.cloud import bigquery
import google.cloud.bigquery.job


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
        print(dataset.name)


def create_dataset(dataset_name, project=None):
    """Craetes a dataset in a given project.

    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)

    dataset = bigquery_client.dataset(dataset_name)

    dataset.create()

    print('Created dataset {}.'.format(dataset_name))


def list_tables(dataset_name, project=None):
    """Lists all of the tables in a given dataset.

    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)
    dataset = bigquery_client.dataset(dataset_name)

    if not dataset.exists():
        print('Dataset {} does not exist.'.format(dataset_name))
        return

    for table in dataset.list_tables():
        print(table.name)


def create_table(dataset_name, table_name, project=None):
    """Creates a simple table in the given dataset.

    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)
    dataset = bigquery_client.dataset(dataset_name)

    if not dataset.exists():
        print('Dataset {} does not exist.'.format(dataset_name))
        return

    table = dataset.table(table_name)

    # Set the table schema
    table.schema = (
        bigquery.SchemaField('Name', 'STRING'),
        bigquery.SchemaField('Age', 'INTEGER'),
        bigquery.SchemaField('Weight', 'FLOAT'),
    )

    table.create()

    print('Created table {} in dataset {}.'.format(table_name, dataset_name))


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

    # Load at most 25 results. You can change the max_results argument to load
    # more rows from BigQuery, but note that this can take some time. It's
    # preferred to use a query.
    rows = list(table.fetch_data(max_results=25))

    # Use format to create a simple table.
    format_string = '{!s:<16} ' * len(table.schema)

    # Print schema field names
    field_names = [field.name for field in table.schema]
    print(format_string.format(*field_names))

    for row in rows:
        print(format_string.format(*row))


def copy_table(dataset_name, table_name, new_table_name, project=None):
    """Copies a table.

    If no project is specified, then the currently active project is used.
    """
    bigquery_client = bigquery.Client(project=project)
    dataset = bigquery_client.dataset(dataset_name)
    table = dataset.table(table_name)

    # This sample shows the destination table in the same dataset and project,
    # however, it's possible to copy across datasets and projects. You can
    # also copy muliple source tables into a single destination table by
    # providing addtional arguments to `copy_table`.
    destination_table = dataset.table(new_table_name)

    # Create a job to copy the table to the destination table.
    job_id = str(uuid.uuid4())
    job = bigquery_client.copy_table(
        job_id, destination_table, table)

    # Create the table if it doesn't exist.
    job.create_disposition = (
        google.cloud.bigquery.job.CreateDisposition.CREATE_IF_NEEDED)

    # Start the job.
    job.begin()

    # Wait for the the job to finish.
    print('Waiting for job to finish...')
    wait_for_job(job)

    print('Table {} copied to {}.'.format(table_name, new_table_name))


def wait_for_job(job):
    while True:
        job.reload()  # Refreshes the state via a GET request.
        if job.state == 'DONE':
            if job.error_result:
                raise RuntimeError(job.errors)
            return
        time.sleep(1)


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

    list_projects_parser = subparsers.add_parser(
        'list-projects', help=list_projects.__doc__)

    list_datasets_parser = subparsers.add_parser(
        'list-datasets', help=list_datasets.__doc__)

    create_dataset_parser = subparsers.add_parser(
        'list-datasets', help=list_datasets.__doc__)
    create_dataset_parser.add_argument('dataset_name')

    list_tables_parser = subparsers.add_parser(
        'list-tables', help=list_tables.__doc__)
    list_tables_parser.add_argument('dataset_name')

    create_table_parser = subparsers.add_parser(
        'create-table', help=create_table.__doc__)
    create_table_parser.add_argument('dataset_name')
    create_table_parser.add_argument('table_name')

    list_rows_parser = subparsers.add_parser(
        'list-rows', help=list_rows.__doc__)
    list_rows_parser.add_argument('dataset_name')
    list_rows_parser.add_argument('table_name')

    copy_table_parser = subparsers.add_parser(
        'copy-table', help=copy_table.__doc__)
    copy_table_parser.add_argument('dataset_name')
    copy_table_parser.add_argument('table_name')
    copy_table_parser.add_argument('new_table_name')

    delete_table_parser = subparsers.add_parser(
        'delete-table', help=delete_table.__doc__)
    delete_table_parser.add_argument('dataset_name')
    delete_table_parser.add_argument('table_name')

    args = parser.parse_args()

    if args.command == 'list-projects':
        list_projects()
    elif args.command == 'list-datasets':
        list_datasets(args.project)
    elif args.command == 'create-dataset':
        create_dataset(args.dataset_name, args.project)
    elif args.command == 'list-tables':
        list_tables(args.dataset_name, args.project)
    elif args.command == 'create-table':
        create_table(args.dataset_name, args.table_name, args.project)
    elif args.command == 'list-rows':
        list_rows(args.dataset_name, args.table_name, args.project)
    elif args.command == 'copy-table':
        copy_table(args.dataset_name, args.table_name, args.new_table_name)
    elif args.command == 'delete-table':
        delete_table(args.dataset_name, args.table_name, args.project)
