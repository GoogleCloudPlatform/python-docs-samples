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

# [START bigquery_drop_procedure]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def drop_procedure(
    project_id: str,
    dataset_id: str,
    procedure_id: str,
) -> None:
    """Drops a GoogleSQL stored procedure from a BigQuery dataset.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID containing the stored procedure
            (for example, 'example_dataset').
        procedure_id: Stored procedure ID to drop
            (for example, 'example_procedure').
    """
    client = bigquery.Client(project=project_id)
    routine_ref = f"{project_id}.{dataset_id}.{procedure_id}"
    # Use IF EXISTS so dropping an already-removed routine succeeds idempotently.
    sql = f"DROP PROCEDURE IF EXISTS `{routine_ref}`;"

    try:
        print(f"Dropping stored procedure: {routine_ref}")
        query_job = client.query(sql)
        query_job.result()
    except exceptions.NotFound as err:
        print(
            f"error: dataset '{dataset_id}' or project '{project_id}' not found: {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to drop stored procedure '{procedure_id}' in dataset "
            f"'{dataset_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {routine_ref}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Statement Type: {query_job.statement_type}")


# [END bigquery_drop_procedure]
