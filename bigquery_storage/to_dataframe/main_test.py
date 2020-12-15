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
        project=your_project_id,
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
    if "country_name" not in out:
        raise AssertionError


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
    if "stackoverflow" not in out:
        raise AssertionError


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
        table,
        parent,
        read_options=read_options,
        # This API can also deliver data serialized in Apache Avro format.
        # This example leverages Apache Arrow.
        format_=bigquery_storage_v1beta1.enums.DataFormat.ARROW,
        # We use a LIQUID strategy in this example because we only read from a
        # single stream. Consider BALANCED if you're consuming multiple streams
        # concurrently and want more consistent stream sizes.
        sharding_strategy=(
            bigquery_storage_v1beta1.enums.ShardingStrategy.LIQUID
        ),
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
    if "species_common_name" not in out:
        raise AssertionError
