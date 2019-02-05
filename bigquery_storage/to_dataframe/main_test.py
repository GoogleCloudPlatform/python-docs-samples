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

import uuid

import pytest


@pytest.fixture
def clients():
    # [START bigquerystorage_pandas_tutorial_create_client]
    import google.auth
    from google.cloud import bigquery
    from google.cloud import bigquery_storage_v1beta1

    # Explicitly create a credentials object. This allows you to use the same
    # credentials for both the BigQuery and BigQuery Storage clients, avoiding
    # unnecessary API calls to fetch duplicate authentication tokens.
    credentials, project_id = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    # Make clients.
    bqclient = bigquery.Client(credentials=credentials, project=project_id)
    bqstorageclient = bigquery_storage_v1beta1.BigQueryStorageClient(
        credentials=credentials
    )
    # [END bigquerystorage_pandas_tutorial_create_client]
    return bqclient, bqstorageclient, project_id


@pytest.fixture
def temporary_dataset(clients):
    bqclient, _, _ = clients
    dataset_id = "bqstorage_to_dataset_{}".format(uuid.uuid4().hex)

    # [START bigquerystorage_pandas_tutorial_create_dataset]
    from google.cloud import bigquery

    # TODO: Set the dataset_id to the dataset used to store temporary results.
    # dataset_id = "query_results_dataset"

    dataset_ref = bqclient.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)

    # Remove tables after 24 hours.
    dataset.default_table_expiration_ms = 1000 * 60 * 60 * 24

    bqclient.create_dataset(dataset)  # API request.
    # [END bigquerystorage_pandas_tutorial_create_dataset]
    yield dataset_id
    bqclient.delete_dataset(dataset_ref, delete_contents=True)


def test_table_to_dataframe(capsys, clients):
    bqclient, bqstorageclient, _ = clients

    # [START bigquerystorage_pandas_tutorial_read_table]
    from google.cloud import bigquery

    # Download a table.
    table = bigquery.TableReference.from_string(
        "bigquery-public-data.utility_us.country_code_iso"
    )
    rows = bqclient.list_rows(
        table,
        selected_fields=[
            bigquery.SchemaField("country_name", "STRING"),
            bigquery.SchemaField("fips_code", "STRING"),
        ],
    )
    dataframe = rows.to_dataframe(bqstorageclient)
    print(dataframe.head())
    # [END bigquerystorage_pandas_tutorial_read_table]

    out, _ = capsys.readouterr()
    assert "country_name" in out


def test_query_to_dataframe(capsys, clients, temporary_dataset):
    bqclient, bqstorageclient, _ = clients
    dataset_id = temporary_dataset

    # [START bigquerystorage_pandas_tutorial_read_query_results]
    import uuid

    from google.cloud import bigquery

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
        destination=table, write_disposition="WRITE_TRUNCATE"
    )

    dataframe = (
        bqclient.query(query_string, job_config=query_config)
        .result()
        .to_dataframe(bqstorageclient)
    )
    print(dataframe.head())
    # [END bigquerystorage_pandas_tutorial_read_query_results]

    out, _ = capsys.readouterr()
    assert "stackoverflow" in out


def test_session_to_dataframe(capsys, clients):
    bqclient, bqstorageclient, project_id = clients

    # [START bigquerystorage_pandas_tutorial_read_session]
    from google.cloud import bigquery_storage_v1beta1

    table = bigquery_storage_v1beta1.types.TableReference()
    table.project_id = "bigquery-public-data"
    table.dataset_id = "new_york_trees"
    table.table_id = "tree_species"

    # Select columns to read with read options. If no read options are
    # specified, the whole table is read.
    read_options = bigquery_storage_v1beta1.types.TableReadOptions()
    read_options.selected_fields.append("species_common_name")
    read_options.selected_fields.append("fall_color")

    parent = "projects/{}".format(project_id)
    session = bqstorageclient.create_read_session(
        table, parent, read_options=read_options
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
    # [END bigquerystorage_pandas_tutorial_read_session]

    out, _ = capsys.readouterr()
    assert "species_common_name" in out
