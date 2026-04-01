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

"""Registers and applies existing BigQuery User-Defined Functions (UDFs) to DataFrames.

Enables the reuse of existing BigQuery SQL or JavaScript UDFs as callable
objects within a BigQuery DataFrames session.
"""

# [START bigquery_dataframes_read_gbq_function]
import bigframes.pandas as bpd


def use_read_gbq_function(project_id: str, function_id: str) -> None:
    bpd.options.bigquery.project = project_id
    bpd.options.bigquery.location = "US"

    # Register an existing BigQuery UDF.
    # The function must have an explicit return type in its BigQuery definition.
    # In production, use functions deployed to your own project for stability.
    extract_title = bpd.read_gbq_function(function_id)

    df = bpd.DataFrame(
        {
            "book_xml": [
                "<book><title>The Great Gatsby</title></book>",
                "<book><title>1984</title></book>",
                "<book><title>Brave New World</title></book>",
            ]
        }
    )

    # Use apply to call the registered BigQuery function for each row.
    # This executes the logic in BigQuery rather than locally.
    df["title"] = df["book_xml"].apply(extract_title)

    print(df[["title"]].to_pandas())


# [END bigquery_dataframes_read_gbq_function]
