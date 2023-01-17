# Copyright 2022 Google LLC
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

# [START enterpriseknowledgegraph_create_entity_reconciliation_job]

from google.cloud import enterpriseknowledgegraph as ekg

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_GRAPH_LOCATION'          # Values: 'global'
# input_dataset = 'YOUR_INPUT_DATASET'      # BigQuery Dataset Name
# input_table = 'YOUR_INPUT_TABLE'          # BigQuery Table Name
# mapping_file_uri = 'YOUR_MAPPING_FILE     # GCS Path. Example: gs://ekg-test-gcs/mapping.yml
# output_dataset = 'YOUR_OUTPUT_DATASET'    # BigQuery Dataset Name

# Refer to https://cloud.google.com/enterprise-knowledge-graph/docs/schema
# entity_type = ekg.InputConfig.EntityType.Person


def create_entity_reconciliation_job_sample(
    project_id: str,
    location: str,
    input_dataset: str,
    input_table: str,
    mapping_file_uri: str,
    entity_type: int,
    output_dataset: str,
) -> None:
    # Create a client
    client = ekg.EnterpriseKnowledgeGraphServiceClient()

    # The full resource name of the location
    # e.g. projects/{project_id}/locations/{location}
    parent = client.common_location_path(project=project_id, location=location)

    # Input Parameters
    input_config = ekg.InputConfig(
        bigquery_input_configs=[
            ekg.BigQueryInputConfig(
                bigquery_table=client.table_path(
                    project=project_id, dataset=input_dataset, table=input_table
                ),
                gcs_uri=mapping_file_uri,
            )
        ],
        entity_type=entity_type,
    )

    # Output Parameters
    output_config = ekg.OutputConfig(
        bigquery_dataset=client.dataset_path(project=project_id, dataset=output_dataset)
    )

    entity_reconciliation_job = ekg.EntityReconciliationJob(
        input_config=input_config, output_config=output_config
    )

    # Initialize request argument(s)
    request = ekg.CreateEntityReconciliationJobRequest(
        parent=parent, entity_reconciliation_job=entity_reconciliation_job
    )

    # Make the request
    response = client.create_entity_reconciliation_job(request=request)

    print(f"Job: {response.name}")
    print(
        f"Input Table: {response.input_config.bigquery_input_configs[0].bigquery_table}"
    )
    print(f"Output Dataset: {response.output_config.bigquery_dataset}")
    print(f"State: {response.state.name}")


# [END enterpriseknowledgegraph_create_entity_reconciliation_job]
