# Copyright 2023 Google LLC
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

import os

import pytest

from discoveryengine import import_documents_sample
from discoveryengine import list_documents_sample

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "global"
data_store_id = "test-structured-data-engine"


def test_import_documents_bigquery():
    # Empty Dataset
    bigquery_dataset = "genappbuilder_test"
    bigquery_table = "import_documents_test"
    operation_name = import_documents_sample.import_documents_bigquery_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        bigquery_dataset=bigquery_dataset,
        bigquery_table=bigquery_table,
    )

    assert "operations/import-documents" in operation_name


def test_import_documents_gcs():
    gcs_uri = "gs://cloud-samples-data/gen-app-builder/search/empty.json"
    operation_name = import_documents_sample.import_documents_gcs_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        gcs_uri=gcs_uri,
    )

    assert "operations/import-documents" in operation_name


@pytest.mark.skip(reason="No Resources")
def test_import_documents_cloud_sql():
    sql_project_id = project_id
    sql_instance_id = "vais-tests"
    sql_database_id = "test-db"
    sql_table_id = "products"
    gcs_staging_dir = "gs://vais-test-staging/"

    operation_name = import_documents_sample.import_documents_cloud_sql_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        sql_project_id=sql_project_id,
        sql_instance_id=sql_instance_id,
        sql_database_id=sql_database_id,
        sql_table_id=sql_table_id,
        gcs_staging_dir=gcs_staging_dir,
    )

    assert "operations/import-documents" in operation_name


@pytest.mark.skip(reason="No Resources")
def test_import_documents_cloud_spanner():
    spanner_project_id = project_id
    spanner_instance_id = "test-instance"
    spanner_database_id = "test-db"
    spanner_table_id = "products"

    operation_name = import_documents_sample.import_documents_cloud_spanner_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        spanner_project_id=spanner_project_id,
        spanner_instance_id=spanner_instance_id,
        spanner_database_id=spanner_database_id,
        spanner_table_id=spanner_table_id,
    )

    assert "operations/import-documents" in operation_name


@pytest.mark.skip(reason="No Resources")
def test_import_documents_firestore():
    firestore_project_id = project_id
    firestore_database_id = "(default)"
    firestore_collection_id = "products"
    gcs_staging_dir = "cloud-samples-data"

    operation_name = import_documents_sample.import_documents_firestore_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        firestore_project_id=firestore_project_id,
        firestore_database_id=firestore_database_id,
        firestore_collection_id=firestore_collection_id,
        gcs_staging_dir=gcs_staging_dir,
    )

    assert "operations/import-documents" in operation_name


@pytest.mark.skip(reason="No Resources")
def test_import_documents_bigtable():
    bigtable_project_id = project_id
    bigtable_instance_id = "test-instance"
    bigtable_table_id = "products"

    operation_name = import_documents_sample.import_documents_bigtable_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        bigtable_project_id=bigtable_project_id,
        bigtable_instance_id=bigtable_instance_id,
        bigtable_table_id=bigtable_table_id,
    )

    assert "operations/import-documents" in operation_name


def test_list_documents():
    response = list_documents_sample.list_documents_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
    )

    assert response
