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


def query_standard_sql(project_id: str = "your-project-id"):
    # [START bigquery_bigframes_query]
    import bigframes.pandas as bpd

    # Set partial ordering mode as the default configuration for BigQuery DataFrames.
    bpd.options.bigquery.ordering_mode = "partial"

    sql = """
    SELECT name FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = 'TX'
    LIMIT 100
    """

    # Run a query alongside existing SQL. The project will be determined from default credentials.
    df = bpd.read_gbq(sql)

    # Run a query after explicitly specifying a project.
    project_id = "your-project-id"
    bpd.options.bigquery.project = project_id
    df = bpd.read_gbq(sql)
    # [END bigquery_bigframes_query]
    return df


def query_legacy_sql():
    # [START bigquery_bigframes_query_legacy]
    import bigframes.pandas as bpd

    # Set partial ordering mode as the default configuration for BigQuery DataFrames.
    bpd.options.bigquery.ordering_mode = "partial"

    sql = """
    SELECT name FROM [bigquery-public-data:usa_names.usa_1910_current]
    WHERE state = 'TX'
    LIMIT 100
    """

    # Run a query using legacy SQL syntax.
    query_config = {"query": {"useLegacySql": True}}
    df = bpd.read_gbq(sql, configuration=query_config)
    # [END bigquery_bigframes_query_legacy]
    return df


def query_bqstorage():
    # [START bigquery_bigframes_query_bqstorage]
    import bigframes.pandas as bpd

    # Set partial ordering mode as the default configuration for BigQuery DataFrames.
    bpd.options.bigquery.ordering_mode = "partial"

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
    # [END bigquery_bigframes_query_bqstorage]
    return pandas_df


def query_parameters():
    # [START bigquery_bigframes_query_parameters]
    import bigframes.pandas as bpd

    # Set partial ordering mode as the default configuration for BigQuery DataFrames.
    bpd.options.bigquery.ordering_mode = "partial"

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
    # [END bigquery_bigframes_query_parameters]
    return df


def upload_from_dataframe(table_id: str = "your-project.your_dataset.your_table_name"):
    # [START bigquery_bigframes_upload_from_dataframe]
    import pandas as pd

    import bigframes.pandas as bpd

    # Set partial ordering mode as the default configuration for BigQuery DataFrames.
    bpd.options.bigquery.ordering_mode = "partial"

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
    table_id = "your-project.your_dataset.your_table_name"
    bq_df.to_gbq(table_id, if_exists="replace")
    # [END bigquery_bigframes_upload_from_dataframe]
    return bq_df
