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

"""Extracts data from XML strings using SQL scalar functions in BigQuery DataFrames.

Demonstrates using BigQuery SQL expressions directly within a DataFrame
transformation for efficient server-side processing.
"""

# [START bigquery_dataframes_sql_scalar]
import bigframes.bigquery as bbq
import bigframes.pandas as bpd


def create_sql_scalar_extraction(project_id: str) -> None:
    bpd.options.bigquery.project = project_id
    bpd.options.bigquery.location = "US"

    df = bpd.DataFrame(
        {
            "book_xml": [
                "<book><title>The Great Gatsby</title></book>",
                "<book><title>1984</title></book>",
                "<book><title>Brave New World</title></book>",
            ]
        }
    )

    # Use bbq.sql_scalar to execute arbitrary SQL expressions directly in BigQuery.
    # The {0} placeholder refers to the first Series in the provided list.
    df["title"] = bbq.sql_scalar(
        "SAFE.REGEXP_EXTRACT({0}, r'<title>(.*?)</title>')",
        [df["book_xml"]],
    )

    print(df[["title"]].to_pandas())


# [END bigquery_dataframes_sql_scalar]
