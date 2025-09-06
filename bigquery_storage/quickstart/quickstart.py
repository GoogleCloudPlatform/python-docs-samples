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


def main(project_id: str = "your-project-id", snapshot_millis: int = 0) -> None:
    # [START bigquerystorage_quickstart]
    from google.cloud.bigquery_storage import BigQueryReadClient, types

    # TODO(developer): Set the project_id variable.
    # project_id = 'your-project-id'
    #
    # The read session is created in this project. This project can be
    # different from that which contains the table.

    client = BigQueryReadClient()

    # This example reads baby name data from the public datasets.
    table = "projects/{}/datasets/{}/tables/{}".format(
        "bigquery-public-data", "usa_names", "usa_1910_current"
    )

    requested_session = types.ReadSession()
    requested_session.table = table
    # This API can also deliver data serialized in Apache Arrow format.
    # This example leverages Apache Avro.
    requested_session.data_format = types.DataFormat.AVRO

    # We limit the output columns to a subset of those allowed in the table,
    # and set a simple filter to only report names from the state of
    # Washington (WA).
    requested_session.read_options.selected_fields = ["name", "number", "state"]
    requested_session.read_options.row_restriction = 'state = "WA"'

    # Set a snapshot time if it's been specified.
    if snapshot_millis > 0:
        snapshot_time = types.Timestamp()
        snapshot_time.FromMilliseconds(snapshot_millis)
        requested_session.table_modifiers.snapshot_time = snapshot_time

    parent = "projects/{}".format(project_id)
    session = client.create_read_session(
        parent=parent,
        read_session=requested_session,
        # We'll use only a single stream for reading data from the table. However,
        # if you wanted to fan out multiple readers you could do so by having a
        # reader process each individual stream.
        max_stream_count=1,
    )
    reader = client.read_rows(session.streams[0].name)

    # The read stream contains blocks of Avro-encoded bytes. The rows() method
    # uses the fastavro library to parse these blocks as an iterable of Python
    # dictionaries. Install fastavro with the following command:
    #
    # pip install google-cloud-bigquery-storage[fastavro]
    rows = reader.rows(session)

    # Do any local processing by iterating over the rows. The
    # google-cloud-bigquery-storage client reconnects to the API after any
    # transient network errors or timeouts.
    names = set()
    states = set()

    # fastavro returns EOFError instead of StopIterationError starting v1.8.4.
    # See https://github.com/googleapis/python-bigquery-storage/pull/687
    try:
        for row in rows:
            names.add(row["name"])
            states.add(row["state"])
    except EOFError:
        pass

    print("Got {} unique names in states: {}".format(len(names), ", ".join(states)))
    # [END bigquerystorage_quickstart]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project_id")
    parser.add_argument("--snapshot_millis", default=0, type=int)
    args = parser.parse_args()
    main(project_id=args.project_id, snapshot_millis=args.snapshot_millis)
