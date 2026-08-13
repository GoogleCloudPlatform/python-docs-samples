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

# [START bigquery_bigframes_table_insert_rows]
import bigframes.pandas as bpd

# Set partial ordering mode as the default configuration for BigQuery
# DataFrames.
bpd.options.bigquery.ordering_mode = "partial"


def table_insert_rows(
    table_id: str = "your-project.your_dataset.your_table_name",
) -> bpd.DataFrame:
    rows_to_insert = [
        {"full_name": "Phred Phlyntstone", "age": 32},
        {"full_name": "Wylma Phlyntstone", "age": 29},
    ]

    # Create a BigQuery DataFrame from the records.
    df = bpd.DataFrame(rows_to_insert)

    # Append rows to the destination BigQuery table.
    df.to_gbq(table_id, if_exists="append")
    return df
# [END bigquery_bigframes_table_insert_rows]


if __name__ == "__main__":
    import os

    table_id = os.environ.get(
        "TABLE_ID", "your-project.your_dataset.your_table_name"
    )
    print(table_insert_rows(table_id=table_id))
