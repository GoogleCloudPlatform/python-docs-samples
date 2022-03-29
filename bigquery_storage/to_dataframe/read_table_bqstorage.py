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


def read_table(your_project_id):
    original_your_project_id = your_project_id
    # [START bigquerystorage_pandas_tutorial_read_session]
    your_project_id = "project-for-read-session"
    # [END bigquerystorage_pandas_tutorial_read_session]
    your_project_id = original_your_project_id

    # [START bigquerystorage_pandas_tutorial_read_session]
    from google.cloud import bigquery_storage
    from google.cloud.bigquery_storage import types
    import pandas

    bqstorageclient = bigquery_storage.BigQueryReadClient()

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
        # Avro is also supported, but the Arrow data format is optimized to
        # work well with column-oriented data structures such as pandas
        # DataFrames.
        data_format=types.DataFormat.ARROW,
        read_options=read_options,
    )
    read_session = bqstorageclient.create_read_session(
        parent=parent,
        read_session=requested_session,
        max_stream_count=1,
    )

    # This example reads from only a single stream. Read from multiple streams
    # to fetch data faster. Note that the session may not contain any streams
    # if there are no rows to read.
    stream = read_session.streams[0]
    reader = bqstorageclient.read_rows(stream.name)

    # Parse all Arrow blocks and create a dataframe.
    frames = []
    for message in reader.rows().pages:
        frames.append(message.to_dataframe())
    dataframe = pandas.concat(frames)
    print(dataframe.head())
    # [END bigquerystorage_pandas_tutorial_read_session]

    return dataframe
