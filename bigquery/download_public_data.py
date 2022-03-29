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


def download_public_data() -> None:

    # [START bigquery_pandas_public_data]

    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the fully-qualified table ID in standard
    # SQL format, including the project ID and dataset ID.
    table_id = "bigquery-public-data.usa_names.usa_1910_current"

    # Use the BigQuery Storage API to speed-up downloads of large tables.
    dataframe = client.list_rows(table_id).to_dataframe(create_bqstorage_client=True)

    print(dataframe.info())
    # [END bigquery_pandas_public_data]
