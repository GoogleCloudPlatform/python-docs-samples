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

# [START bigquery_federated_view_schema_spanner]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def federated_view_schema_spanner(
    project_id: str,
    connection_id: str,
) -> None:
    """Views a Cloud Spanner table schema from BigQuery using EXTERNAL_QUERY.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        connection_id: Fully qualified BigQuery Cloud Spanner connection ID
            (for example, 'example-project.us.example-spanner-conn').
    """
    client = bigquery.Client(project=project_id)
    # Query Spanner information_schema.columns inside EXTERNAL_QUERY to inspect table column metadata.
    external_sql = (
        "SELECT column_name, spanner_type, is_nullable "
        "FROM information_schema.columns "
        "WHERE table_name = 'orders' "
        "ORDER BY ordinal_position ASC"
    )
    query = f"""
        SELECT
          column_name,
          spanner_type,
          is_nullable
        FROM EXTERNAL_QUERY('{connection_id}', "{external_sql}")
        ORDER BY column_name ASC;
    """

    try:
        print(f"Inspecting Spanner table schema via connection: {connection_id}")
        query_job = client.query(query)
        rows = list(query_job.result())
    except exceptions.NotFound as err:
        print(
            f"error: Spanner connection '{connection_id}' not found in project "
            f"'{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: could not inspect Spanner table schema on connection "
            f"'{connection_id}' in project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {connection_id}")
    print(f"Columns Returned: {len(rows)}")
    print(f"Job ID: {query_job.job_id}")


# [END bigquery_federated_view_schema_spanner]
