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

import argparse


def main(project_id="your-project-id", snapshot_millis=0):
    # [START bigquerystorage_quickstart]
    from google.cloud import bigquery_storage_v1beta1

    # TODO(developer): Set the project_id variable.
    # project_id = 'your-project-id'
    #
    # The read session is created in this project. This project can be
    # different from that which contains the table.

    client = bigquery_storage_v1beta1.BigQueryStorageClient()

    # This example reads baby name data from the public datasets.
    table_ref = bigquery_storage_v1beta1.types.TableReference()
    table_ref.project_id = "bigquery-public-data"
    table_ref.dataset_id = "usa_names"
    table_ref.table_id = "usa_1910_current"

    # We limit the output columns to a subset of those allowed in the table,
    # and set a simple filter to only report names from the state of
    # Washington (WA).
    read_options = bigquery_storage_v1beta1.types.TableReadOptions()
    read_options.selected_fields.append("name")
    read_options.selected_fields.append("number")
    read_options.selected_fields.append("state")
    read_options.row_restriction = 'state = "WA"'

    # Set a snapshot time if it's been specified.
    modifiers = None
    if snapshot_millis > 0:
        modifiers = bigquery_storage_v1beta1.types.TableModifiers()
        modifiers.snapshot_time.FromMilliseconds(snapshot_millis)

    parent = "projects/{}".format(project_id)
    session = client.create_read_session(
        table_ref,
        parent,
        table_modifiers=modifiers,
        read_options=read_options,
        # This API can also deliver data serialized in Apache Arrow format.
        # This example leverages Apache Avro.
        format_=bigquery_storage_v1beta1.enums.DataFormat.AVRO,
        # We use a LIQUID strategy in this example because we only read from a
        # single stream. Consider BALANCED if you're consuming multiple streams
        # concurrently and want more consistent stream sizes.
        sharding_strategy=(bigquery_storage_v1beta1.enums.ShardingStrategy.LIQUID),
    )  # API request.

    # We'll use only a single stream for reading data from the table. Because
    # of dynamic sharding, this will yield all the rows in the table. However,
    # if you wanted to fan out multiple readers you could do so by having a
    # reader process each individual stream.
    reader = client.read_rows(
        bigquery_storage_v1beta1.types.StreamPosition(stream=session.streams[0])
    )

    # The read stream contains blocks of Avro-encoded bytes. The rows() method
    # uses the fastavro library to parse these blocks as an interable of Python
    # dictionaries. Install fastavro with the following command:
    #
    # pip install google-cloud-bigquery-storage[fastavro]
    rows = reader.rows(session)

    # Do any local processing by iterating over the rows. The
    # google-cloud-bigquery-storage client reconnects to the API after any
    # transient network errors or timeouts.
    names = set()
    states = set()

    for row in rows:
        names.add(row["name"])
        states.add(row["state"])

    print("Got {} unique names in states: {}".format(len(names), states))
    # [END bigquerystorage_quickstart]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project_id")
    parser.add_argument("--snapshot_millis", default=0, type=int)
    args = parser.parse_args()
    main(project_id=args.project_id)
