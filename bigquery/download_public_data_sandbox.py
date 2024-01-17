# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def download_public_data_sandbox() -> None:
    # [START bigquery_pandas_public_data_sandbox]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # `SELECT *` is an anti-pattern in BigQuery because it is cheaper and
    # faster to use the BigQuery Storage API directly, but BigQuery Sandbox
    # users can only use the BigQuery Storage API to download query results.
    query_string = "SELECT * FROM `bigquery-public-data.usa_names.usa_1910_current`"

    # Use the BigQuery Storage API to speed-up downloads of large tables.
    dataframe = client.query_and_wait(query_string).to_dataframe(
        create_bqstorage_client=True
    )

    print(dataframe.info())
    # [END bigquery_pandas_public_data_sandbox]
