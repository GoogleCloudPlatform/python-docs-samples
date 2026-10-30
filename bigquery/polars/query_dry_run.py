# Copyright 2026 Google LLC
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

# [START bigquery_polars_query_dry_run]
import polars
import polars_bigquery


def construct_client(
    project_id: str = "your-project-id",
) -> polars_bigquery.Client:
    """Constructs a Polars BigQuery client."""
    return polars_bigquery.Client(
        quota_project_id=project_id,
    )


def query_dry_run(plbq: polars_bigquery.Client) -> polars.DataFrame:
    """Estimates the bytes processed by a SQL query using a dry run."""
    sql = """
    SELECT name, SUM(number) AS total_people
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = 'TX'
    GROUP BY name
    """

    # Perform a dry run to validate the query and estimate bytes processed
    # without executing the query.
    stats = plbq.read_query(
        sql,
        dry_run=True,
        use_query_cache=False,
    )
    total_bytes = stats.item(0, "totalBytesProcessed")
    print(f"This query will process {total_bytes} bytes.")
    return stats


# [END bigquery_polars_query_dry_run]


if __name__ == "__main__":
    import os

    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    query_dry_run(construct_client(project_id=project))
