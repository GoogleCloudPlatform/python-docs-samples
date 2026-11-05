# Copyright 2026 Google LLC
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

# [START bigquery_call_system_procedure]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def call_system_procedure(
    project_id: str,
    dataset_id: str,
    materialized_view_id: str,
) -> None:
    """Calls the BQ.REFRESH_MATERIALIZED_VIEW system procedure with a query parameter.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID containing the materialized view
            (for example, 'example_dataset').
        materialized_view_id: Materialized view ID to refresh
            (for example, 'example_mv').
    """
    client = bigquery.Client(project=project_id)
    mv_ref = f"{project_id}.{dataset_id}.{materialized_view_id}"
    # Pass the target materialized view identifier via a query parameter to BQ.REFRESH_MATERIALIZED_VIEW.
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("view_name", "STRING", mv_ref),
        ]
    )
    sql = "CALL BQ.REFRESH_MATERIALIZED_VIEW(@view_name);"

    try:
        print(f"Refreshing materialized view via system procedure: {mv_ref}")
        query_job = client.query(sql, job_config=job_config)
        query_job.result()
    except exceptions.NotFound as err:
        print(
            f"error: materialized view '{materialized_view_id}' not found in dataset "
            f"'{dataset_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to refresh materialized view '{materialized_view_id}' in dataset "
            f"'{dataset_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {mv_ref}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Statement Type: {query_job.statement_type}")
    print("System Procedure: BQ.REFRESH_MATERIALIZED_VIEW")


# [END bigquery_call_system_procedure]
