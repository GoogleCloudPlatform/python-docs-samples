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

# [START bigquery_bigframes_query_parameters]
import bigframes.pandas as bpd

# Set partial ordering mode as the default configuration for BigQuery
# DataFrames.
bpd.options.bigquery.ordering_mode = "partial"


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
