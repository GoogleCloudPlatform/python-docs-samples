# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START bigquery_migration_create_workflow]
def create_migration_workflow(
    gcs_input_path: str, gcs_output_path: str, project_id: str
) -> None:
    """Creates a migration workflow of a Batch SQL Translation and prints the response."""

    from google.cloud import bigquery_migration_v2

    parent = f"projects/{project_id}/locations/us"

    # Construct a BigQuery Migration client object.
    client = bigquery_migration_v2.MigrationServiceClient()

    # Set the source dialect to Teradata SQL.
    source_dialect = bigquery_migration_v2.Dialect()
    source_dialect.teradata_dialect = bigquery_migration_v2.TeradataDialect(
        mode=bigquery_migration_v2.TeradataDialect.Mode.SQL
    )

    # Set the target dialect to BigQuery dialect.
    target_dialect = bigquery_migration_v2.Dialect()
    target_dialect.bigquery_dialect = bigquery_migration_v2.BigQueryDialect()

    # Prepare the config proto.
    translation_config = bigquery_migration_v2.TranslationConfigDetails(
        gcs_source_path=gcs_input_path,
        gcs_target_path=gcs_output_path,
        source_dialect=source_dialect,
        target_dialect=target_dialect,
    )

    # Prepare the task.
    migration_task = bigquery_migration_v2.MigrationTask(
        type_="Translation_Teradata2BQ", translation_config_details=translation_config
    )

    # Prepare the workflow.
    workflow = bigquery_migration_v2.MigrationWorkflow(
        display_name="demo-workflow-python-example-Teradata2BQ"
    )

    workflow.tasks["translation-task"] = migration_task  # type: ignore

    # Prepare the API request to create a migration workflow.
    request = bigquery_migration_v2.CreateMigrationWorkflowRequest(
        parent=parent,
        migration_workflow=workflow,
    )

    response = client.create_migration_workflow(request=request)

    print("Created workflow:")
    print(response.display_name)
    print("Current state:")
    print(response.State(response.state))


# [END bigquery_migration_create_workflow]
