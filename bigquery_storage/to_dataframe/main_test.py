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
    # [START bigquerystorage_pandas_tutorial_all]
    # [START bigquerystorage_pandas_tutorial_create_client]
    import google.auth
    from google.cloud import bigquery
    from google.cloud import bigquery_storage_v1beta1

    # Explicitly create a credentials object. This allows you to use the same
    # credentials for both the BigQuery and BigQuery Storage clients, avoiding
    # unnecessary API calls to fetch duplicate authentication tokens.
    credentials, your_project_id = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    # Make clients.
    bqclient = bigquery.Client(
        credentials=credentials,
        project=your_project_id
    )
    bqstorageclient = bigquery_storage_v1beta1.BigQueryStorageClient(
        credentials=credentials
    )
    # [END bigquerystorage_pandas_tutorial_create_client]
    # [END bigquerystorage_pandas_tutorial_all]
    return bqclient, bqstorageclient


def test_table_to_dataframe(capsys, clients):
    from google.cloud import bigquery

    bqclient, bqstorageclient = clients

    # [START bigquerystorage_pandas_tutorial_all]
    # [START bigquerystorage_pandas_tutorial_read_table]
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
    dataframe = rows.to_dataframe(bqstorage_client=bqstorageclient)
    print(dataframe.head())
    # [END bigquerystorage_pandas_tutorial_read_table]
    # [END bigquerystorage_pandas_tutorial_all]

    out, _ = capsys.readouterr()
    assert "country_name" in out


@pytest.fixture
def temporary_dataset(clients):
    from google.cloud import bigquery

    bqclient, _ = clients

    # [START bigquerystorage_pandas_tutorial_all]
    # [START bigquerystorage_pandas_tutorial_create_dataset]
    # Set the dataset_id to the dataset used to store temporary results.
    dataset_id = "query_results_dataset"
    # [END bigquerystorage_pandas_tutorial_create_dataset]
    # [END bigquerystorage_pandas_tutorial_all]

    dataset_id = "bqstorage_to_dataset_{}".format(uuid.uuid4().hex)

    # [START bigquerystorage_pandas_tutorial_all]
    # [START bigquerystorage_pandas_tutorial_create_dataset]
    dataset_ref = bqclient.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)

    # Remove tables after 24 hours.
    dataset.default_table_expiration_ms = 1000 * 60 * 60 * 24

    bqclient.create_dataset(dataset)  # API request.
    # [END bigquerystorage_pandas_tutorial_create_dataset]
    # [END bigquerystorage_pandas_tutorial_all]
    yield dataset_ref
    # [START bigquerystorage_pandas_tutorial_cleanup]
    bqclient.delete_dataset(dataset_ref, delete_contents=True)
    # [END bigquerystorage_pandas_tutorial_cleanup]


def test_query_to_dataframe(capsys, clients, temporary_dataset):
    from google.cloud import bigquery

    bqclient, bqstorageclient = clients
    dataset_ref = temporary_dataset

    # [START bigquerystorage_pandas_tutorial_all]
    # [START bigquerystorage_pandas_tutorial_read_query_results]
    import uuid

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
    # Use a random table name to avoid overwriting existing tables.
    table_id = "queryresults_" + uuid.uuid4().hex
    table = dataset_ref.table(table_id)
    query_config = bigquery.QueryJobConfig(
        # Due to a known issue in the BigQuery Storage API, small query result
        # sets cannot be downloaded. To workaround this issue, write results to
        # a destination table.
        destination=table
    )

    dataframe = (
        bqclient.query(query_string, job_config=query_config)
        .result()
        .to_dataframe(bqstorage_client=bqstorageclient)
    )
    print(dataframe.head())
    # [END bigquerystorage_pandas_tutorial_read_query_results]
    # [END bigquerystorage_pandas_tutorial_all]

    out, _ = capsys.readouterr()
    assert "stackoverflow" in out


def test_session_to_dataframe(capsys, clients):
    from google.cloud import bigquery_storage_v1beta1

    bqclient, bqstorageclient = clients
    your_project_id = bqclient.project

    # [START bigquerystorage_pandas_tutorial_all]
    # [START bigquerystorage_pandas_tutorial_read_session]
    table = bigquery_storage_v1beta1.types.TableReference()
    table.project_id = "bigquery-public-data"
    table.dataset_id = "new_york_trees"
    table.table_id = "tree_species"

    # Select columns to read with read options. If no read options are
    # specified, the whole table is read.
    read_options = bigquery_storage_v1beta1.types.TableReadOptions()
    read_options.selected_fields.append("species_common_name")
    read_options.selected_fields.append("fall_color")

    parent = "projects/{}".format(your_project_id)
    session = bqstorageclient.create_read_session(
        table, parent, read_options=read_options
    )

    # This example reads from only a single stream. Read from multiple streams
    # to fetch data faster. Note that the session may not contain any streams
    # if there are no rows to read.
    stream = session.streams[0]
    position = bigquery_storage_v1beta1.types.StreamPosition(stream=stream)
    reader = bqstorageclient.read_rows(position)

    # Parse all Avro blocks and create a dataframe. This call requires a
    # session, because the session contains the schema for the row blocks.
    dataframe = reader.to_dataframe(session)
    print(dataframe.head())
    # [END bigquerystorage_pandas_tutorial_read_session]
    # [END bigquerystorage_pandas_tutorial_all]

    out, _ = capsys.readouterr()
    assert "species_common_name" in out
