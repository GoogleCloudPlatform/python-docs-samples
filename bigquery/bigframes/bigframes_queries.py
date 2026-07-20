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


import bigframes.pandas as bpd
import pandas as pd

# Set partial ordering mode as the default configuration for BigQuery DataFrames.
bpd.options.bigquery.ordering_mode = "partial"


# [START bigquery_bigframes_query]
def query_standard_sql(project_id: str = "your-project-id") -> bpd.DataFrame:
    sql = """
    SELECT name FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = 'TX'
    LIMIT 100
    """

    # Run a query alongside existing SQL. The project will be determined from default credentials.
    df = bpd.read_gbq(sql)

    # Run a query after explicitly specifying a project.
    bpd.close_session()
    bpd.options.bigquery.project = project_id
    df = bpd.read_gbq(sql)
    return df


# [END bigquery_bigframes_query]


# [START bigquery_bigframes_query_bqstorage]
def query_bqstorage() -> pd.DataFrame:
    sql = """
    SELECT name FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = 'TX'
    LIMIT 100
    """

    # Read query results into a server-side DataFrame without downloading data.
    df = bpd.read_gbq(sql)

    # When downloading results to an in-memory pandas DataFrame, bigquery-dataframes
    # automatically uses the BigQuery Storage API if installed.
    pandas_df = df.to_pandas()
    return pandas_df


# [END bigquery_bigframes_query_bqstorage]


# [START bigquery_bigframes_query_parameters]
def query_parameters() -> bpd.DataFrame:
    sql = """
    SELECT name FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = @state
    LIMIT 100
    """

    query_config = {
        "query": {
            "parameterMode": "NAMED",
            "queryParameters": [
                {
                    "name": "state",
                    "parameterType": {"type": "STRING"},
                    "parameterValue": {"value": "TX"},
                }
            ],
        }
    }

    df = bpd.read_gbq(sql, configuration=query_config)
    return df


# [END bigquery_bigframes_query_parameters]


# [START bigquery_bigframes_upload_from_dataframe]
def upload_from_dataframe(
    table_id: str = "your-project.your_dataset.your_table_name",
) -> bpd.DataFrame:
    # Create a local pandas DataFrame.
    df = pd.DataFrame(
        {
            "my_string": ["a", "b", "c"],
            "my_int64": [1, 2, 3],
            "my_float64": [4.0, 5.0, 6.0],
        }
    )

    # Convert the local pandas DataFrame to a BigQuery DataFrame.
    bq_df = bpd.read_pandas(df)

    # Write the DataFrame to a BigQuery table.
    bq_df.to_gbq(table_id, if_exists="replace")
    return bq_df


# [END bigquery_bigframes_upload_from_dataframe]
