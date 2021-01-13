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

import pytest


@pytest.fixture
def clients():
    # [START bigquerystorage_pandas_tutorial_all]
    # [START bigquerystorage_pandas_tutorial_create_client]
    import google.auth
    from google.cloud import bigquery
    from google.cloud import bigquery_storage

    # Explicitly create a credentials object. This allows you to use the same
    # credentials for both the BigQuery and BigQuery Storage clients, avoiding
    # unnecessary API calls to fetch duplicate authentication tokens.
    credentials, your_project_id = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    # Make clients.
    bqclient = bigquery.Client(credentials=credentials, project=your_project_id,)
    bqstorageclient = bigquery_storage.BigQueryReadClient(credentials=credentials)
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


def test_query_to_dataframe(capsys, clients):
    bqclient, bqstorageclient = clients

    # [START bigquerystorage_pandas_tutorial_all]
    # [START bigquerystorage_pandas_tutorial_read_query_results]
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

    dataframe = (
        bqclient.query(query_string)
        .result()
        .to_dataframe(bqstorage_client=bqstorageclient)
    )
    print(dataframe.head())
    # [END bigquerystorage_pandas_tutorial_read_query_results]
    # [END bigquerystorage_pandas_tutorial_all]

    out, _ = capsys.readouterr()
    assert "stackoverflow" in out


def test_session_to_dataframe(capsys, clients):
    from google.cloud.bigquery_storage import types

    bqclient, bqstorageclient = clients
    your_project_id = bqclient.project

    # [START bigquerystorage_pandas_tutorial_all]
    # [START bigquerystorage_pandas_tutorial_read_session]
    project_id = "bigquery-public-data"
    dataset_id = "new_york_trees"
    table_id = "tree_species"
    table = f"projects/{project_id}/datasets/{dataset_id}/tables/{table_id}"

    # Select columns to read with read options. If no read options are
    # specified, the whole table is read.
    read_options = types.ReadSession.TableReadOptions(
        selected_fields=["species_common_name", "fall_color"]
    )

    parent = "projects/{}".format(your_project_id)

    requested_session = types.ReadSession(
        table=table,
        # This API can also deliver data serialized in Apache Avro format.
        # This example leverages Apache Arrow.
        data_format=types.DataFormat.ARROW,
        read_options=read_options,
    )
    read_session = bqstorageclient.create_read_session(
        parent=parent, read_session=requested_session, max_stream_count=1,
    )

    # This example reads from only a single stream. Read from multiple streams
    # to fetch data faster. Note that the session may not contain any streams
    # if there are no rows to read.
    stream = read_session.streams[0]
    reader = bqstorageclient.read_rows(stream.name)

    # Parse all Arrow blocks and create a dataframe. This call requires a
    # session, because the session contains the schema for the row blocks.
    dataframe = reader.to_dataframe(read_session)
    print(dataframe.head())
    # [END bigquerystorage_pandas_tutorial_read_session]
    # [END bigquerystorage_pandas_tutorial_all]

    out, _ = capsys.readouterr()
    assert "species_common_name" in out
