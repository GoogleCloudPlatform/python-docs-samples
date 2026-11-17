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

# [START bigquery_search_exclude_columns]
from google.cloud import bigquery


def search_exclude_columns(
    project_id: str,
) -> None:
    """Searches a BigQuery table while excluding specific columns using EXCEPT.

    Args:
        project_id: Google Cloud project ID used to bill the query job
            (for example, 'example-project').
    """
    client = bigquery.Client(project=project_id)
    # Query the public theLook eCommerce dataset in bigquery-public-data
    # (https://cloud.google.com/bigquery/public-data).
    table_ref = "bigquery-public-data.thelook_ecommerce.users"
    # Exclude street_address, city, state, and country from the searched fields using SELECT AS STRUCT ... EXCEPT.
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
          u.email
        FROM `{table_ref}` AS u
        WHERE SEARCH(
          (SELECT AS STRUCT u.* EXCEPT (street_address, city, state, country)),
          @search_query
        )
        ORDER BY u.id ASC
        LIMIT 10;
    """

    print(f"Searching {table_ref} excluding address columns for term: {search_query}")
    query_job = client.query(sql, job_config=job_config)
    rows = list(query_job.result())

    print(f"Resource ID: {table_ref}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Matching Rows: {len(rows)}")
    print(f"Search Term: {search_query}")


# [END bigquery_search_exclude_columns]
