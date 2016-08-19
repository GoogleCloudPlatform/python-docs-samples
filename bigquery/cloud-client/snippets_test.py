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

from gcloud import bigquery
import pytest
import snippets


DATASET_ID = 'test_dataset'
TABLE_ID = 'test_import_table'


@pytest.mark.xfail(
    strict=True,
    reason='https://github.com/GoogleCloudPlatform/gcloud-python/issues/2143')
def test_list_projects():
    snippets.list_projects()
    # No need to check the ouput, lack of exception is enough.


def test_list_datasets(capsys):
    # Requires the dataset to have been created in the test project.
    snippets.list_datasets()

    out, _ = capsys.readouterr()

    assert DATASET_ID in out


def test_list_tables(capsys):
    # Requires teh dataset and table to have been created in the test project.
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


def test_delete_table(capsys):
    # Create a table to delete
    bigquery_client = bigquery.Client()
    dataset = bigquery_client.dataset(DATASET_ID)
    table = dataset.table('test_delete_table')

    if not table.exists():
        table.schema = [bigquery.SchemaField('id', 'INTEGER')]
        table.create()

    snippets.delete_table(DATASET_ID, table.name)

    assert not table.exists()
