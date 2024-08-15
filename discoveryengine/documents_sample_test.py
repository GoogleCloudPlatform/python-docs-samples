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

from discoveryengine import import_documents_sample
from discoveryengine import list_documents_sample
from discoveryengine import purge_documents_sample

import pytest

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
    gcs_uri = "gs://cloud-samples-data/gen-app-builder/search/alphabet-investor-pdfs/goog023-alphabet-2023-annual-report-web-1.pdf"
    operation_name = import_documents_sample.import_documents_gcs_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        gcs_uri=gcs_uri,
    )

    assert "operations/import-documents" in operation_name


@pytest.mark.skip(reason="Permissions")
def test_import_documents_cloud_sql():
    sql_project_id = project_id
    sql_instance_id = "vertex-ai-search-tests"
    sql_database_id = "test-db"
    sql_table_id = "products"

    operation_name = import_documents_sample.import_documents_cloud_sql_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        sql_project_id=sql_project_id,
        sql_instance_id=sql_instance_id,
        sql_database_id=sql_database_id,
        sql_table_id=sql_table_id,
    )

    assert "operations/import-documents" in operation_name


def test_import_documents_spanner():
    spanner_project_id = project_id
    spanner_instance_id = "test-instance"
    spanner_database_id = "vais-test-db"
    spanner_table_id = "products"

    operation_name = import_documents_sample.import_documents_spanner_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        spanner_project_id=spanner_project_id,
        spanner_instance_id=spanner_instance_id,
        spanner_database_id=spanner_database_id,
        spanner_table_id=spanner_table_id,
    )

    assert "operations/import-documents" in operation_name


def test_import_documents_firestore():
    firestore_project_id = project_id
    firestore_database_id = "vais-tests"
    firestore_collection_id = "products"

    operation_name = import_documents_sample.import_documents_firestore_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        firestore_project_id=firestore_project_id,
        firestore_database_id=firestore_database_id,
        firestore_collection_id=firestore_collection_id,
    )

    assert "operations/import-documents" in operation_name


@pytest.mark.skip(reason="Timeout")
def test_import_documents_bigtable():
    bigtable_project_id = project_id
    bigtable_instance_id = "bigtable-test"
    bigtable_table_id = "vais-test"

    operation_name = import_documents_sample.import_documents_bigtable_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        bigtable_project_id=bigtable_project_id,
        bigtable_instance_id=bigtable_instance_id,
        bigtable_table_id=bigtable_table_id,
    )

    assert "operations/import-documents" in operation_name


def test_import_documents_alloy_db():
    operation_name = import_documents_sample.import_documents_alloy_db_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        alloy_db_project_id=project_id,
        alloy_db_location_id="us-central1",
        alloy_db_cluster_id="vais-tests",
        alloy_db_database_id="postgres",
        alloy_db_table_id="public.vais",
    )

    assert "operations/import-documents" in operation_name


@pytest.mark.skip(reason="Permissions")
def test_import_documents_healthcare_fhir_sample():
    location = "us"
    data_store_id = "healthcare-search-test"
    healthcare_project_id = project_id
    healthcare_location = "us-central1"
    healthcare_dataset_id = "vais_testing"
    healthcare_fihr_store_id = "vais_test_fihr_data"

    operation_name = import_documents_sample.import_documents_healthcare_fhir_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
        healthcare_project_id=healthcare_project_id,
        healthcare_location=healthcare_location,
        healthcare_dataset_id=healthcare_dataset_id,
        healthcare_fihr_store_id=healthcare_fihr_store_id,
    )

    assert "operations/import-documents" in operation_name


def test_list_documents():
    response = list_documents_sample.list_documents_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
    )

    assert response


def test_purge_documents():
    response = purge_documents_sample.purge_documents_sample(
        project_id=project_id,
        location=location,
        data_store_id=data_store_id,
    )

    assert response
