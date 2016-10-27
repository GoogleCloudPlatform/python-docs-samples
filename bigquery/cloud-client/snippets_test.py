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

from google.cloud import bigquery
import pytest

import snippets


DATASET_ID = 'test_dataset'
TABLE_ID = 'test_table'


def test_list_projects():
    snippets.list_projects()
    # No need to check the ouput, lack of exception is enough.


def test_list_datasets(capsys):
    # Requires the dataset to have been created in the test project.
    snippets.list_datasets()

    out, _ = capsys.readouterr()

    assert DATASET_ID in out


@pytest.fixture
def cleanup_dataset():
    dataset_name = 'test_temporary_dataset'
    bigquery_client = bigquery.Client()
    dataset = bigquery_client.dataset(dataset_name)

    if dataset.exists():
        dataset.delete()

    yield dataset_name

    if dataset.exists():
        dataset.delete()


def test_create_dataset(capsys, cleanup_dataset):
    snippets.create_dataset(cleanup_dataset)

    out, _ = capsys.readouterr()

    assert cleanup_dataset in out


def test_list_tables(capsys):
    # Requires the dataset and table to have been created in the test project.
    snippets.list_tables(DATASET_ID)

    out, _ = capsys.readouterr()

    assert TABLE_ID in out


def test_list_rows(capsys):
    # Requires the dataset and table to have been created in the test project.

    # Check for the schema. It's okay if the table is empty as long as there
    # aren't any errors.

    snippets.list_rows(DATASET_ID, TABLE_ID)

    out, _ = capsys.readouterr()

    assert 'Name' in out
    assert 'Age' in out


@pytest.fixture
def temporary_table():
    """Fixture that returns a factory for tables that do not yet exist and
    will be automatically deleted after the test."""
    bigquery_client = bigquery.Client()
    dataset = bigquery_client.dataset(DATASET_ID)
    tables = []

    def factory(table_name):
        new_table = dataset.table(table_name)
        if new_table.exists():
            new_table.delete()
        tables.append(new_table)
        return new_table

    yield factory

    for table in tables:
        if table.exists():
            table.delete()


def test_create_table(temporary_table):
    new_table = temporary_table('test_create_table')
    snippets.create_table(DATASET_ID, new_table.name)
    assert new_table.exists()


@pytest.mark.slow
def test_copy_table(temporary_table):
    new_table = temporary_table('test_copy_table')
    snippets.copy_table(DATASET_ID, TABLE_ID, new_table.name)
    assert new_table.exists()


def test_delete_table():
    # Create a table to delete
    bigquery_client = bigquery.Client()
    dataset = bigquery_client.dataset(DATASET_ID)
    table = dataset.table('test_delete_table')

    if not table.exists():
        table.schema = [bigquery.SchemaField('id', 'INTEGER')]
        table.create()

    snippets.delete_table(DATASET_ID, table.name)

    assert not table.exists()
