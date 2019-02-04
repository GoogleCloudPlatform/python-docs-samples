# Copyright 2019 Google LLC
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


def main(dataset_id="query_results"):
    # [START bigquerystorage_pandas_create_client]
    import google.auth
    from google.cloud import bigquery
    from google.cloud import bigquery_storage_v1beta1

    # Explicitly create a credentials object. This allows you to use the same
    # credentials for both the BigQuery and BigQuery Storage clients, avoiding
    # unnecessary API calls to fetch duplicate authentication tokens.
    credentials, project_id = google.auth.default(
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    # Make clients.
    bqclient = bigquery.Client(credentials=credentials, project=project_id)
    bqstorageclient = bigquery_storage_v1beta1.BigQueryStorageClient(
        credentials=credentials)
    # [END bigquerystorage_pandas_create_client]

    # [START bigquerystorage_pandas_read_table]
    # Download a table.
    table = bqclient.get_table(
        "bigquery-public-data.utility_us.country_code_iso"
    )
    rows = bqclient.list_rows(table)
    dataframe = rows.to_dataframe(bqstorageclient)
    print(dataframe.head())
    # [END bigquerystorage_pandas_read_table]

    dataset = bqclient.dataset(dataset_id)

    # [START bigquerystorage_pandas_read_query_results]
    # Download query results.
    query_string = """
SELECT
  CONCAT(
    'https://stackoverflow.com/questions/',
    CAST(id as STRING)) as url,
  view_count
FROM `bigquery-public-data.stackoverflow.posts_questions`
WHERE tags like '%google-bigquery%'
ORDER BY view_count DESC
"""
    query_config = bigquery.QueryJobConfig(
        # Due to a known issue in the BigQuery Storage API (TODO: link to
        # public issue), small result sets cannot be downloaded. To workaround
        # this issue, write your results to a destination table.
        destination=dataset.table('query_results_table'),
        write_disposition="WRITE_TRUNCATE"
    )

    dataframe = (
        bqclient.query(query_string, job_config=query_config)
        .result()
        .to_dataframe(bqstorageclient)
    )
    print(dataframe.head())
    # [END bigquerystorage_pandas_read_query_results]

    # [START bigquerystorage_pandas_read_session]
    table = bigquery_storage_v1beta1.types.TableReference()
    table.project_id = "bigquery-public-data"
    table.dataset_id = "utility_us"
    table.table_id = "country_code_iso"

    parent = "projects/{}".format(project_id)
    session = bqstorageclient.create_read_session(table, parent)

    # Don't try to read from an empty table.
    if len(session.streams) == 0:
        return

    # This example reads from only a single stream. Read from multiple streams
    # to fetch data faster.
    stream = session.streams[0]
    position = bigquery_storage_v1beta1.types.StreamPosition(stream=stream)
    reader = bqstorageclient.read_rows(position)

    # Parse all Avro blocks and create a dataframe. This call requires a
    # session, because the session contains the schema for the row blocks.
    dataframe = reader.to_dataframe(session)
    print(dataframe.head())
    # [END bigquerystorage_pandas_read_session]


if __name__ == "__main__":
    main()
