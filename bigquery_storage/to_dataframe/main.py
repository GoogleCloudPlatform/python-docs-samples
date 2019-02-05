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

import argparse


def main(dataset_id="query_results"):
    print("Creating clients.")
    bqclient, bqstorageclient, project_id = create_clients()
    print("\n\nReading a table:")
    table_to_dataframe(bqclient, bqstorageclient)
    print("\n\nReading query results:")
    query_to_dataframe(bqclient, bqstorageclient, dataset_id)
    print("\n\nReading a table, using the BQ Storage API directly:")
    session_to_dataframe(bqstorageclient, project_id)


def create_clients():
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
    return bqclient, bqstorageclient, project_id


def table_to_dataframe(bqclient, bqstorageclient):
    from google.cloud import bigquery

    # [START bigquerystorage_pandas_read_table]
    # Download a table.
    table = bigquery.TableReference.from_string(
        "bigquery-public-data.utility_us.country_code_iso"
    )
    rows = bqclient.list_rows(
        table,
        selected_fields=[
            bigquery.SchemaField("country_name", "STRING"),
            bigquery.SchemaField("fips_code", "STRING"),
        ]
    )
    dataframe = rows.to_dataframe(bqstorageclient)
    print(dataframe.head())
    # [END bigquerystorage_pandas_read_table]


def query_to_dataframe(bqclient, bqstorageclient, dataset_id):
    from google.cloud import bigquery

    # [START bigquerystorage_pandas_read_query_results]
    import uuid

    # Due to a known issue in the BigQuery Storage API (TODO: link to
    # public issue), small query result sets cannot be downloaded. To
    # workaround this issue, write results to a destination table.

    # TODO: Set dataset_id to a dataset that will store temporary query
    #       results. Set the default table expiration time to ensure data is
    #       deleted after the results have been downloaded.
    # dataset_id = "temporary_dataset_for_query_results"
    dataset = bqclient.dataset(dataset_id)
    table_id = "queryresults_" + uuid.uuid4().hex
    table = dataset.table(table_id)

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
        destination=table,
        write_disposition="WRITE_TRUNCATE"
    )

    dataframe = (
        bqclient.query(query_string, job_config=query_config)
        .result()
        .to_dataframe(bqstorageclient)
    )
    print(dataframe.head())
    # [END bigquerystorage_pandas_read_query_results]


def session_to_dataframe(bqstorageclient, project_id):
    from google.cloud import bigquery_storage_v1beta1

    # [START bigquerystorage_pandas_read_session]
    table = bigquery_storage_v1beta1.types.TableReference()
    table.project_id = "bigquery-public-data"
    table.dataset_id = "new_york_trees"
    table.table_id = "tree_species"

    # Specify read options to select columns to read. If no read options are
    # specified, the whole table is read.
    read_options = bigquery_storage_v1beta1.types.TableReadOptions()
    read_options.selected_fields.append("species_common_name")
    read_options.selected_fields.append("fall_color")

    parent = "projects/{}".format(project_id)
    session = bqstorageclient.create_read_session(
        table,
        parent,
        read_options=read_options
    )

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
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_id')
    args = parser.parse_args()
    main(args.dataset_id)
