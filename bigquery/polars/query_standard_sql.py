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

# [START bigquery_polars_query]
import polars
import polars_bigquery


def construct_client(project_id: str = "your-project-id") -> polars_bigquery.Client:
    return polars_bigquery.Client(
        quota_project_id=project_id,
    )


def query_standard_sql(plbq: polars_bigquery.Client) -> polars.DataFrame:
    sql = """
    SELECT name, sum(number) as total_people
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = 'TX'
    GROUP BY name
    ORDER BY total_people DESC
    LIMIT 100
    """

    # Run a query and immediately download the results.
    df = plbq.read_query(
        sql,
        # For the best performance, set maintain_order=False if you don't care
        # about the order of the rows in the result.
        maintain_order=True,
    )
    return df
# [END bigquery_polars_query]


if __name__ == "__main__":
    import os

    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    print(query_standard_sql(construct_client(project_id=project)))
