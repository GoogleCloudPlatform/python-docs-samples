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

# [START bigquery_call_procedure]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def call_procedure(
    project_id: str,
    dataset_id: str,
    procedure_id: str,
) -> None:
    """Calls a GoogleSQL stored procedure with input and output parameters.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID containing the stored procedure
            (for example, 'example_dataset').
        procedure_id: Stored procedure ID to invoke
            (for example, 'example_procedure').
    """
    client = bigquery.Client(project=project_id)
    routine_ref = f"{project_id}.{dataset_id}.{procedure_id}"
    # Bind the input filter value via a query parameter to prevent SQL injection.
    target_corpus = "hamlet"
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("target_corpus", "STRING", target_corpus),
        ]
    )
    sql = f"""
        DECLARE out_total INT64;
        CALL `{routine_ref}`(@target_corpus, out_total);
        SELECT out_total AS total_words;
    """

    try:
        print(f"Calling stored procedure: {routine_ref}")
        query_job = client.query(sql, job_config=job_config)
        rows = list(query_job.result())
    except exceptions.NotFound as err:
        print(
            f"error: stored procedure '{procedure_id}' not found in dataset "
            f"'{dataset_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to call stored procedure '{procedure_id}' in dataset "
            f"'{dataset_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    total_words = rows[0].total_words if rows else 0
    print(f"Resource ID: {routine_ref}")
    print(f"Corpus: {target_corpus}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Total Words: {total_words}")


# [END bigquery_call_procedure]
