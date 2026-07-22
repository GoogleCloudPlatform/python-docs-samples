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

# [START bigquery_bigframes_query_bqstorage]
import bigframes.pandas as bpd

import pandas as pd

# Set partial ordering mode as the default configuration for BigQuery
# DataFrames.
bpd.options.bigquery.ordering_mode = "partial"


def query_bqstorage() -> pd.DataFrame:
    sql = """
    SELECT name FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = 'TX'
    LIMIT 100
    """

    # Read query results into a server-side DataFrame without downloading data.
    df = bpd.read_gbq(sql)

    # When downloading results to an in-memory pandas DataFrame,
    # bigquery-dataframes automatically uses the BigQuery Storage API if
    # installed.
    pandas_df = df.to_pandas()
    return pandas_df
# [END bigquery_bigframes_query_bqstorage]
