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

# [START bigquery_polars_query_bqstorage]
import polars
import polars_bigquery


def construct_client(project_id: str = "your-project-id") -> polars_bigquery.Client:
    return polars_bigquery.Client(
        quota_project_id=project_id,
    )


def query_bqstorage(plbq: polars_bigquery.Client) -> polars.DataFrame:
    sql = """
    SELECT year, name, SUM(number)
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    GROUP BY year, name
    """

    # Run a query and immediately download the results. polars-biqquery
    # automatically uses the BigQuery Storage Read API to download results that
    # don't fit in a single response message.
    df = plbq.read_query(
        sql,
        # For the best performance, set maintain_order=False if you don't care
        # about the order of the rows in the result. This allows polars-bigquery
        # to create multiple BigQuery Storage Read API read streams if needed.
        maintain_order=False,
    )
    return df
# [END bigquery_polars_query_bqstorage]


if __name__ == "__main__":
    import os

    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    print(query_bqstorage(construct_client(project)))
