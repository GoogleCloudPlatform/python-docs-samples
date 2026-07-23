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

# [START bigquery_bigframes_upload_from_dataframe]
import bigframes.pandas as bpd

import pandas as pd

# Set partial ordering mode as the default configuration for BigQuery
# DataFrames.
bpd.options.bigquery.ordering_mode = "partial"


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


if __name__ == "__main__":
    import os

    table_id = os.environ.get(
        "TABLE_ID", "your-project.your_dataset.your_table_name"
    )
    print(upload_from_dataframe(table_id=table_id))
