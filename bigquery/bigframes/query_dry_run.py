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

# [START bigquery_bigframes_query_dry_run]
from typing import Tuple

import bigframes.pandas as bpd
import pandas as pd

# Set partial ordering mode as the default configuration for BigQuery
# DataFrames.
bpd.options.bigquery.ordering_mode = "partial"


def query_dry_run(
    project_id: str = "your-project-id",
) -> Tuple[pd.Series, pd.Series]:
    """Estimates the bytes processed by a SQL query and a DataFrame operation."""
    bpd.options.bigquery.project = project_id

    sql = """
    SELECT name, SUM(number) AS total_people
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = 'TX'
    GROUP BY name
    """

    # Perform a dry run on a SQL query without executing it.
    sql_stats = bpd.read_gbq(sql, use_cache=False, dry_run=True)
    print(f"SQL query will process {sql_stats['totalBytesProcessed']} bytes.")

    # Perform a dry run on BigQuery DataFrames operations before downloading
    # results to an in-memory pandas DataFrame.
    df = bpd.read_gbq("bigquery-public-data.usa_names.usa_1910_current")
    df_tx = df[df["state"] == "TX"].groupby("name", as_index=False)["number"].sum()
    df_stats = df_tx.to_pandas(dry_run=True)
    print(f"DataFrame operation will process {df_stats['totalBytesProcessed']} bytes.")

    return sql_stats, df_stats


# [END bigquery_bigframes_query_dry_run]


if __name__ == "__main__":
    import os

    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    query_dry_run(project_id=project)
