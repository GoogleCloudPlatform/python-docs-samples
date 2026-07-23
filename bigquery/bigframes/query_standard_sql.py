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

# [START bigquery_bigframes_query]
import bigframes.pandas as bpd

# Set partial ordering mode as the default configuration for BigQuery
# DataFrames.
bpd.options.bigquery.ordering_mode = "partial"


def query_standard_sql(project_id: str = "your-project-id") -> bpd.DataFrame:
    sql = """
    SELECT name FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = 'TX'
    LIMIT 100
    """

    # Run a query alongside existing SQL. The project will be determined from
    # default credentials.
    df = bpd.read_gbq(sql)

    # Run a query after explicitly specifying a project.
    bpd.close_session()
    bpd.options.bigquery.project = project_id
    df = bpd.read_gbq(sql)
    return df
# [END bigquery_bigframes_query]


if __name__ == "__main__":
    import os

    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    print(query_standard_sql(project_id=project))
