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

# [START bigquery_migration_pandas_gbq_query_dry_run]
import pandas as pd
import pandas_gbq


def query_dry_run(project_id: str = "your-project-id") -> pd.Series:
    """Estimates the bytes processed by a SQL query using a dry run."""
    sql = """
    SELECT name, SUM(number) AS total_people
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = 'TX'
    GROUP BY name
    """

    # Perform a dry run to estimate bytes processed without running the query.
    query_config = {
        "query": {
            "useQueryCache": False,
        }
    }
    stats = pandas_gbq.read_gbq(
        sql,
        project_id=project_id,
        configuration=query_config,
        dry_run=True,
    )
    print(f"This query will process {stats['totalBytesProcessed']} bytes.")
    return stats


# [END bigquery_migration_pandas_gbq_query_dry_run]


if __name__ == "__main__":
    import os

    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    query_dry_run(project_id=project)
