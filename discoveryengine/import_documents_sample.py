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

# [START genappbuilder_import_documents]


def import_documents_bigquery_sample(
    project_id: str,
    location: str,
    data_store_id: str,
    bigquery_dataset: str,
    bigquery_table: str,
) -> str:
    # [START genappbuilder_import_documents_bigquery]

    from google.api_core.client_options import ClientOptions
    from google.cloud import discoveryengine

    # TODO(developer): Uncomment these variables before running the sample.
    # project_id = "YOUR_PROJECT_ID"
    # location = "YOUR_LOCATION" # Values: "global"
    # data_store_id = "YOUR_DATA_STORE_ID"
    # bigquery_dataset = "YOUR_BIGQUERY_DATASET"
    # bigquery_table = "YOUR_BIGQUERY_TABLE"

    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.DocumentServiceClient(client_options=client_options)

    # The full resource name of the search engine branch.
    # e.g. projects/{project}/locations/{location}/dataStores/{data_store_id}/branches/{branch}
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        branch="default_branch",
    )

    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        bigquery_source=discoveryengine.BigQuerySource(
            project_id=project_id,
            dataset_id=bigquery_dataset,
            table_id=bigquery_table,
            data_schema="custom",
        ),
        # Options: `FULL`, `INCREMENTAL`
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    # Make the request
    operation = client.import_documents(request=request)

    print(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()

    # After the operation is complete,
    # get information from operation metadata
    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

    # Handle the response
    print(response)
    print(metadata)
    # [END genappbuilder_import_documents_bigquery]

    return operation.operation.name


def import_documents_gcs_sample(
    project_id: str,
    location: str,
    data_store_id: str,
    gcs_uri: str,
) -> str:
    # [START genappbuilder_import_documents_gcs]
    from google.api_core.client_options import ClientOptions
    from google.cloud import discoveryengine

    # TODO(developer): Uncomment these variables before running the sample.
    # project_id = "YOUR_PROJECT_ID"
    # location = "YOUR_LOCATION" # Values: "global"
    # data_store_id = "YOUR_DATA_STORE_ID"

    # Examples:
    # - Unstructured documents
    #   - `gs://bucket/directory/file.pdf`
    #   - `gs://bucket/directory/*.pdf`
    # - Unstructured documents with JSONL Metadata
    #   - `gs://bucket/directory/file.json`
    # - Unstructured documents with CSV Metadata
    #   - `gs://bucket/directory/file.csv`
    # gcs_uri = "YOUR_GCS_PATH"

    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.DocumentServiceClient(client_options=client_options)

    # The full resource name of the search engine branch.
    # e.g. projects/{project}/locations/{location}/dataStores/{data_store_id}/branches/{branch}
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        branch="default_branch",
    )

    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        gcs_source=discoveryengine.GcsSource(
            # Multiple URIs are supported
            input_uris=[gcs_uri],
            # Options:
            # - `content` - Unstructured documents (PDF, HTML, DOC, TXT, PPTX)
            # - `custom` - Unstructured documents with custom JSONL metadata
            # - `document` - Structured documents in the discoveryengine.Document format.
            # - `csv` - Unstructured documents with CSV metadata
            data_schema="content",
        ),
        # Options: `FULL`, `INCREMENTAL`
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    # Make the request
    operation = client.import_documents(request=request)

    print(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()

    # After the operation is complete,
    # get information from operation metadata
    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

    # Handle the response
    print(response)
    print(metadata)
    # [END genappbuilder_import_documents_gcs]

    return operation.operation.name


# [END genappbuilder_import_documents]


def import_documents_cloud_sql_sample(
    project_id: str,
    location: str,
    data_store_id: str,
    sql_project_id: str,
    sql_instance_id: str,
    sql_database_id: str,
    sql_table_id: str,
) -> str:
    # [START genappbuilder_import_documents_cloud_sql]
    from google.api_core.client_options import ClientOptions
    from google.cloud import discoveryengine

    # TODO(developer): Uncomment these variables before running the sample.
    # project_id = "YOUR_PROJECT_ID"
    # location = "YOUR_LOCATION" # Values: "global"
    # data_store_id = "YOUR_DATA_STORE_ID"
    # sql_project_id = "YOUR_SQL_PROJECT_ID"
    # sql_instance_id = "YOUR_SQL_INSTANCE_ID"
    # sql_database_id = "YOUR_SQL_DATABASE_ID"
    # sql_table_id = "YOUR_SQL_TABLE_ID"

    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.DocumentServiceClient(client_options=client_options)

    # The full resource name of the search engine branch.
    # e.g. projects/{project}/locations/{location}/dataStores/{data_store_id}/branches/{branch}
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        branch="default_branch",
    )

    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        cloud_sql_source=discoveryengine.CloudSqlSource(
            project_id=sql_project_id,
            instance_id=sql_instance_id,
            database_id=sql_database_id,
            table_id=sql_table_id,
        ),
        # Options: `FULL`, `INCREMENTAL`
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    # Make the request
    operation = client.import_documents(request=request)

    print(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()

    # After the operation is complete,
    # get information from operation metadata
    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

    # Handle the response
    print(response)
    print(metadata)
    # [END genappbuilder_import_documents_cloud_sql]

    return operation.operation.name


def import_documents_spanner_sample(
    project_id: str,
    location: str,
    data_store_id: str,
    spanner_project_id: str,
    spanner_instance_id: str,
    spanner_database_id: str,
    spanner_table_id: str,
) -> str:
    # [START genappbuilder_import_documents_spanner]
    from google.api_core.client_options import ClientOptions
    from google.cloud import discoveryengine

    # TODO(developer): Uncomment these variables before running the sample.
    # project_id = "YOUR_PROJECT_ID"
    # location = "YOUR_LOCATION" # Values: "global"
    # data_store_id = "YOUR_DATA_STORE_ID"
    # spanner_project_id = "YOUR_SPANNER_PROJECT_ID"
    # spanner_instance_id = "YOUR_SPANNER_INSTANCE_ID"
    # spanner_database_id = "YOUR_SPANNER_DATABASE_ID"
    # spanner_table_id = "YOUR_SPANNER_TABLE_ID"

    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.DocumentServiceClient(client_options=client_options)

    # The full resource name of the search engine branch.
    # e.g. projects/{project}/locations/{location}/dataStores/{data_store_id}/branches/{branch}
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        branch="default_branch",
    )

    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        spanner_source=discoveryengine.SpannerSource(
            project_id=spanner_project_id,
            instance_id=spanner_instance_id,
            database_id=spanner_database_id,
            table_id=spanner_table_id,
        ),
        # Options: `FULL`, `INCREMENTAL`
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    # Make the request
    operation = client.import_documents(request=request)

    print(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()

    # After the operation is complete,
    # get information from operation metadata
    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

    # Handle the response
    print(response)
    print(metadata)
    # [END genappbuilder_import_documents_spanner]

    return operation.operation.name


def import_documents_firestore_sample(
    project_id: str,
    location: str,
    data_store_id: str,
    firestore_project_id: str,
    firestore_database_id: str,
    firestore_collection_id: str,
) -> str:
    # [START genappbuilder_import_documents_firestore]
    from google.api_core.client_options import ClientOptions
    from google.cloud import discoveryengine

    # TODO(developer): Uncomment these variables before running the sample.
    # project_id = "YOUR_PROJECT_ID"
    # location = "YOUR_LOCATION" # Values: "global"
    # data_store_id = "YOUR_DATA_STORE_ID"
    # firestore_project_id = "YOUR_FIRESTORE_PROJECT_ID"
    # firestore_database_id = "YOUR_FIRESTORE_DATABASE_ID"
    # firestore_collection_id = "YOUR_FIRESTORE_COLLECTION_ID"

    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.DocumentServiceClient(client_options=client_options)

    # The full resource name of the search engine branch.
    # e.g. projects/{project}/locations/{location}/dataStores/{data_store_id}/branches/{branch}
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        branch="default_branch",
    )

    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        firestore_source=discoveryengine.FirestoreSource(
            project_id=firestore_project_id,
            database_id=firestore_database_id,
            collection_id=firestore_collection_id,
        ),
        # Options: `FULL`, `INCREMENTAL`
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    # Make the request
    operation = client.import_documents(request=request)

    print(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()

    # After the operation is complete,
    # get information from operation metadata
    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

    # Handle the response
    print(response)
    print(metadata)
    # [END genappbuilder_import_documents_firestore]

    return operation.operation.name


def import_documents_bigtable_sample(
    project_id: str,
    location: str,
    data_store_id: str,
    bigtable_project_id: str,
    bigtable_instance_id: str,
    bigtable_table_id: str,
) -> str:
    # [START genappbuilder_import_documents_bigtable]
    from google.api_core.client_options import ClientOptions
    from google.cloud import discoveryengine

    # TODO(developer): Uncomment these variables before running the sample.
    # project_id = "YOUR_PROJECT_ID"
    # location = "YOUR_LOCATION" # Values: "global"
    # data_store_id = "YOUR_DATA_STORE_ID"
    # bigtable_project_id = "YOUR_BIGTABLE_PROJECT_ID"
    # bigtable_instance_id = "YOUR_BIGTABLE_INSTANCE_ID"
    # bigtable_table_id = "YOUR_BIGTABLE_TABLE_ID"

    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.DocumentServiceClient(client_options=client_options)

    # The full resource name of the search engine branch.
    # e.g. projects/{project}/locations/{location}/dataStores/{data_store_id}/branches/{branch}
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        branch="default_branch",
    )

    bigtable_options = discoveryengine.BigtableOptions(
        families={
            "family_name_1": discoveryengine.BigtableOptions.BigtableColumnFamily(
                type_=discoveryengine.BigtableOptions.Type.STRING,
                encoding=discoveryengine.BigtableOptions.Encoding.TEXT,
                columns=[
                    discoveryengine.BigtableOptions.BigtableColumn(
                        qualifier="qualifier_1".encode("utf-8"),
                        field_name="field_name_1",
                    ),
                ],
            ),
            "family_name_2": discoveryengine.BigtableOptions.BigtableColumnFamily(
                type_=discoveryengine.BigtableOptions.Type.INTEGER,
                encoding=discoveryengine.BigtableOptions.Encoding.BINARY,
            ),
        }
    )

    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        bigtable_source=discoveryengine.BigtableSource(
            project_id=bigtable_project_id,
            instance_id=bigtable_instance_id,
            table_id=bigtable_table_id,
            bigtable_options=bigtable_options,
        ),
        # Options: `FULL`, `INCREMENTAL`
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    # Make the request
    operation = client.import_documents(request=request)

    print(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()

    # After the operation is complete,
    # get information from operation metadata
    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

    # Handle the response
    print(response)
    print(metadata)
    # [END genappbuilder_import_documents_bigtable]

    return operation.operation.name


def import_documents_alloy_db_sample(
    project_id: str,
    location: str,
    data_store_id: str,
    alloy_db_project_id: str,
    alloy_db_location_id: str,
    alloy_db_cluster_id: str,
    alloy_db_database_id: str,
    alloy_db_table_id: str,
) -> str:
    # [START genappbuilder_import_documents_alloy_db]
    from google.api_core.client_options import ClientOptions
    from google.cloud import discoveryengine_v1 as discoveryengine

    # TODO(developer): Uncomment these variables before running the sample.
    # project_id = "YOUR_PROJECT_ID"
    # location = "YOUR_LOCATION" # Values: "global"
    # data_store_id = "YOUR_DATA_STORE_ID"
    # alloy_db_project_id = "YOUR_ALLOY_DB_PROJECT_ID"
    # alloy_db_location_id = "YOUR_ALLOY_DB_LOCATION_ID"
    # alloy_db_cluster_id = "YOUR_ALLOY_DB_CLUSTER_ID"
    # alloy_db_database_id = "YOUR_ALLOY_DB_DATABASE_ID"
    # alloy_db_table_id = "YOUR_ALLOY_DB_TABLE_ID"

    # For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.DocumentServiceClient(client_options=client_options)

    # The full resource name of the search engine branch.
    # e.g. projects/{project}/locations/{location}/dataStores/{data_store_id}/branches/{branch}
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        branch="default_branch",
    )

    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        alloy_db_source=discoveryengine.AlloyDbSource(
            project_id=alloy_db_project_id,
            location_id=alloy_db_location_id,
            cluster_id=alloy_db_cluster_id,
            database_id=alloy_db_database_id,
            table_id=alloy_db_table_id,
        ),
        # Options: `FULL`, `INCREMENTAL`
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    # Make the request
    operation = client.import_documents(request=request)

    print(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()

    # After the operation is complete,
    # get information from operation metadata
    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

    # Handle the response
    print(response)
    print(metadata)
    # [END genappbuilder_import_documents_alloy_db]

    return operation.operation.name


def import_documents_healthcare_fhir_sample(
    project_id: str,
    location: str,
    data_store_id: str,
    healthcare_project_id: str,
    healthcare_location: str,
    healthcare_dataset_id: str,
    healthcare_fihr_store_id: str,
) -> str:
    # [START genappbuilder_import_documents_healthcare_fhir]
    from google.api_core.client_options import ClientOptions
    from google.cloud import discoveryengine

    # TODO(developer): Uncomment these variables before running the sample.
    # project_id = "YOUR_PROJECT_ID"
    # location = "YOUR_LOCATION" # Values: "us"
    # data_store_id = "YOUR_DATA_STORE_ID"
    # healthcare_project_id = "YOUR_HEALTHCARE_PROJECT_ID"
    # healthcare_location = "YOUR_HEALTHCARE_LOCATION"
    # healthcare_dataset_id = "YOUR_HEALTHCARE_DATASET_ID"
    # healthcare_fihr_store_id = "YOUR_HEALTHCARE_FHIR_STORE_ID"

    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.DocumentServiceClient(client_options=client_options)

    # The full resource name of the search engine branch.
    # e.g. projects/{project}/locations/{location}/dataStores/{data_store_id}/branches/{branch}
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        branch="default_branch",
    )

    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        fhir_store_source=discoveryengine.FhirStoreSource(
            fhir_store=client.fhir_store_path(
                healthcare_project_id,
                healthcare_location,
                healthcare_dataset_id,
                healthcare_fihr_store_id,
            ),
        ),
        # Options: `FULL`, `INCREMENTAL`
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    # Make the request
    operation = client.import_documents(request=request)

    print(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()

    # After the operation is complete,
    # get information from operation metadata
    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

    # Handle the response
    print(response)
    print(metadata)
    # [END genappbuilder_import_documents_healthcare_fhir]

    return operation.operation.name
