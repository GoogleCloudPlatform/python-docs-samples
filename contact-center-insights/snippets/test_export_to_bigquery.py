# Copyright 2021 Google LLC
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
#
import uuid

import google.auth
from google.cloud import bigquery
import pytest

import export_to_bigquery

GCLOUD_TESTS_PREFIX = "python_samples_tests"


@pytest.fixture
def project_id():
    _, project_id = google.auth.default()
    return project_id


@pytest.fixture
def unique_id():
    uuid_hex = uuid.uuid4().hex[:8]
    return f"{GCLOUD_TESTS_PREFIX}_{uuid_hex}"


@pytest.fixture
def bigquery_resources(project_id, unique_id):
    # Create a BigQuery dataset.
    bigquery_client = bigquery.Client()
    dataset_id = unique_id
    table_id = unique_id

    dataset = bigquery.Dataset(f"{project_id}.{dataset_id}")
    dataset.location = "US"
    bigquery_client.create_dataset(dataset, timeout=30)

    # Create a BigQuery table under the created dataset.
    table = bigquery.Table(f"{project_id}.{dataset_id}.{table_id}")
    bigquery_client.create_table(table)

    yield dataset_id, table_id

    # Delete the BigQuery dataset and table.
    bigquery_client.delete_dataset(dataset_id, delete_contents=True)


def test_export_data_to_bigquery(capsys, project_id, bigquery_resources):
    dataset_id, table_id = bigquery_resources
    export_to_bigquery.export_to_bigquery(project_id, project_id, dataset_id, table_id)
    out, err = capsys.readouterr()
    assert "Exported data to BigQuery" in out
