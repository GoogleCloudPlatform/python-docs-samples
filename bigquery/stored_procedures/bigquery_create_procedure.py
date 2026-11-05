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

# [START bigquery_create_procedure]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def create_procedure(
    project_id: str,
    dataset_id: str,
) -> None:
    """Creates a GoogleSQL stored procedure in a BigQuery dataset.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        dataset_id: BigQuery dataset ID where the procedure is created
            (for example, 'example_dataset').
    """
    client = bigquery.Client(project=project_id)
    # Use a fixed procedure identifier inside the caller-supplied dataset.
    # The procedure body queries the public Shakespeare dataset in bigquery-public-data
    # (https://cloud.google.com/bigquery/public-data).
    procedure_id = "example_procedure"
    routine_ref = f"{project_id}.{dataset_id}.{procedure_id}"
    sql = f"""
        CREATE OR REPLACE PROCEDURE `{routine_ref}`(
          target_corpus STRING,
          OUT total_words INT64
        )
        BEGIN
          SET total_words = (
            SELECT COALESCE(SUM(word_count), 0)
            FROM `bigquery-public-data.samples.shakespeare`
            WHERE corpus = target_corpus
          );
        END;
    """

    try:
        print(f"Creating stored procedure: {routine_ref}")
        query_job = client.query(sql)
        query_job.result()
    except exceptions.NotFound as err:
        print(
            f"error: dataset '{dataset_id}' not found in project '{project_id}' "
            f"when creating stored procedure '{procedure_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to create stored procedure '{procedure_id}' in dataset "
            f"'{dataset_id}' for project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {routine_ref}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Procedure ID: {procedure_id}")
    print(f"Statement Type: {query_job.statement_type}")


# [END bigquery_create_procedure]
