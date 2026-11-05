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

# [START bigquery_search_with_text_analyzer]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def search_with_text_analyzer(
    project_id: str,
) -> None:
    """Searches a BigQuery column using an explicit text analyzer in SEARCH.

    Args:
        project_id: Google Cloud project ID used to bill the query job
            (for example, 'example-project').
    """
    client = bigquery.Client(project=project_id)
    # Query the public theLook eCommerce dataset in bigquery-public-data
    # (https://cloud.google.com/bigquery/public-data).
    table_ref = "bigquery-public-data.thelook_ecommerce.users"
    # Specify NO_OP_ANALYZER so SEARCH performs exact case-sensitive substring matching without tokenizing.
    analyzer_name = "NO_OP_ANALYZER"
    search_query = "Nelson Apt"
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("search_query", "STRING", search_query),
        ]
    )
    sql = f"""
        SELECT
          u.id,
          u.first_name,
          u.last_name,
          u.street_address
        FROM `{table_ref}` AS u
        WHERE SEARCH(u.street_address, @search_query, analyzer => '{analyzer_name}')
        ORDER BY u.id ASC
        LIMIT 10;
    """

    try:
        print(
            f"Searching {table_ref} with analyzer {analyzer_name} for: {search_query}"
        )
        query_job = client.query(sql, job_config=job_config)
        rows = list(query_job.result())
    except exceptions.NotFound as err:
        print(
            f"error: table '{table_ref}' not found when querying from project "
            f"'{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to search '{table_ref}' with analyzer '{analyzer_name}' "
            f"in project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {table_ref}")
    print(f"Analyzer: {analyzer_name}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Matching Rows: {len(rows)}")


# [END bigquery_search_with_text_analyzer]
