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

# [START bigquery_federated_query_cloud_sql]
import sys

from google.api_core import exceptions
from google.cloud import bigquery


def federated_query_cloud_sql(
    project_id: str,
    connection_id: str,
) -> None:
    """Runs a federated query from BigQuery to Cloud SQL using EXTERNAL_QUERY.

    Args:
        project_id: Google Cloud project ID (for example, 'example-project').
        connection_id: Fully qualified BigQuery Cloud SQL connection ID
            (for example, 'example-project.us.example-cloudsql-conn').
    """
    client = bigquery.Client(project=project_id)
    # EXTERNAL_QUERY pushes the order aggregation and filter down to Cloud SQL,
    # then joins the summarized results with the public theLook eCommerce users table
    # in bigquery-public-data (https://cloud.google.com/bigquery/public-data).
    external_sql = (
        "SELECT user_id, COUNT(order_id) AS completed_orders, "
        "MIN(created_at) AS first_order_date "
        "FROM orders WHERE status = 'Complete' GROUP BY user_id"
    )
    query = f"""
        SELECT
          u.id AS user_id,
          u.country,
          rq.completed_orders,
          rq.first_order_date
        FROM EXTERNAL_QUERY('{connection_id}', "{external_sql}") AS rq
        INNER JOIN `bigquery-public-data.thelook_ecommerce.users` AS u
          ON u.id = rq.user_id
        ORDER BY user_id ASC
        LIMIT 10;
    """

    try:
        print(f"Running Cloud SQL federated query via connection: {connection_id}")
        query_job = client.query(query)
        rows = list(query_job.result())
    except exceptions.NotFound as err:
        print(
            f"error: Cloud SQL connection '{connection_id}' not found in project "
            f"'{project_id}': {err.message}",
            file=sys.stderr,
        )
        return
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: could not run Cloud SQL federated query on connection "
            f"'{connection_id}' in project '{project_id}': {err.message}",
            file=sys.stderr,
        )
        return

    print(f"Resource ID: {connection_id}")
    print(f"Job ID: {query_job.job_id}")
    print(f"Rows Returned: {len(rows)}")


# [END bigquery_federated_query_cloud_sql]
