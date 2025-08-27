# Copyright 2021 Google LLC
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

# [START bigquerystorage_append_rows_raw_proto2]
"""
This code sample demonstrates using the low-level generated client for Python.
"""

import datetime
import decimal

from google.cloud import bigquery_storage_v1
from google.cloud.bigquery_storage_v1 import types, writer
from google.protobuf import descriptor_pb2

# If you make updates to the sample_data.proto protocol buffers definition,
# run:
#
#   protoc --python_out=. sample_data.proto
#
# from the samples/snippets directory to generate the sample_data_pb2 module.
from . import sample_data_pb2


def append_rows_proto2(project_id: str, dataset_id: str, table_id: str) -> None:
    """Create a write stream, write some sample data, and commit the stream."""
    write_client = bigquery_storage_v1.BigQueryWriteClient()
    parent = write_client.table_path(project_id, dataset_id, table_id)
    write_stream = types.WriteStream()

    # When creating the stream, choose the type. Use the PENDING type to wait
    # until the stream is committed before it is visible. See:
    # https://cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1#google.cloud.bigquery.storage.v1.WriteStream.Type
    write_stream.type_ = types.WriteStream.Type.PENDING
    write_stream = write_client.create_write_stream(
        parent=parent, write_stream=write_stream
    )
    stream_name = write_stream.name

    # Create a template with fields needed for the first request.
    request_template = types.AppendRowsRequest()

    # The initial request must contain the stream name.
    request_template.write_stream = stream_name

    # So that BigQuery knows how to parse the serialized_rows, generate a
    # protocol buffer representation of your message descriptor.
    proto_schema = types.ProtoSchema()
    proto_descriptor = descriptor_pb2.DescriptorProto()
    sample_data_pb2.SampleData.DESCRIPTOR.CopyToProto(proto_descriptor)
    proto_schema.proto_descriptor = proto_descriptor
    proto_data = types.AppendRowsRequest.ProtoData()
    proto_data.writer_schema = proto_schema
    request_template.proto_rows = proto_data

    # Some stream types support an unbounded number of requests. Construct an
    # AppendRowsStream to send an arbitrary number of requests to a stream.
    append_rows_stream = writer.AppendRowsStream(write_client, request_template)

    # Create a batch of row data by appending proto2 serialized bytes to the
    # serialized_rows repeated field.
    proto_rows = types.ProtoRows()

    row = sample_data_pb2.SampleData()
    row.row_num = 1
    row.bool_col = True
    row.bytes_col = b"Hello, World!"
    row.float64_col = float("+inf")
    row.int64_col = 123
    row.string_col = "Howdy!"
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 2
    row.bool_col = False
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 3
    row.bytes_col = b"See you later!"
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 4
    row.float64_col = 1000000.125
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 5
    row.int64_col = 67000
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 6
    row.string_col = "Auf Wiedersehen!"
    proto_rows.serialized_rows.append(row.SerializeToString())

    # Set an offset to allow resuming this stream if the connection breaks.
    # Keep track of which requests the server has acknowledged and resume the
    # stream at the first non-acknowledged message. If the server has already
    # processed a message with that offset, it will return an ALREADY_EXISTS
    # error, which can be safely ignored.
    #
    # The first request must always have an offset of 0.
    request = types.AppendRowsRequest()
    request.offset = 0
    proto_data = types.AppendRowsRequest.ProtoData()
    proto_data.rows = proto_rows
    request.proto_rows = proto_data

    response_future_1 = append_rows_stream.send(request)

    # Create a batch of rows containing scalar values that don't directly
    # correspond to a protocol buffers scalar type. See the documentation for
    # the expected data formats:
    # https://cloud.google.com/bigquery/docs/write-api#data_type_conversions
    proto_rows = types.ProtoRows()

    row = sample_data_pb2.SampleData()
    row.row_num = 7
    date_value = datetime.date(2021, 8, 12)
    epoch_value = datetime.date(1970, 1, 1)
    delta = date_value - epoch_value
    row.date_col = delta.days
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 8
    datetime_value = datetime.datetime(2021, 8, 12, 9, 46, 23, 987456)
    row.datetime_col = datetime_value.strftime("%Y-%m-%d %H:%M:%S.%f")
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 9
    row.geography_col = "POINT(-122.347222 47.651111)"
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 10
    numeric_value = decimal.Decimal("1.23456789101112e+6")
    row.numeric_col = str(numeric_value)
    bignumeric_value = decimal.Decimal("-1.234567891011121314151617181920e+16")
    row.bignumeric_col = str(bignumeric_value)
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 11
    time_value = datetime.time(11, 7, 48, 123456)
    row.time_col = time_value.strftime("%H:%M:%S.%f")
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 12
    timestamp_value = datetime.datetime(
        2021, 8, 12, 16, 11, 22, 987654, tzinfo=datetime.timezone.utc
    )
    epoch_value = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    delta = timestamp_value - epoch_value
    row.timestamp_col = int(delta.total_seconds()) * 1000000 + int(delta.microseconds)
    proto_rows.serialized_rows.append(row.SerializeToString())

    # Since this is the second request, you only need to include the row data.
    # The name of the stream and protocol buffers DESCRIPTOR is only needed in
    # the first request.
    request = types.AppendRowsRequest()
    proto_data = types.AppendRowsRequest.ProtoData()
    proto_data.rows = proto_rows
    request.proto_rows = proto_data

    # Offset must equal the number of rows that were previously sent.
    request.offset = 6

    response_future_2 = append_rows_stream.send(request)

    # Create a batch of rows with STRUCT and ARRAY BigQuery data types. In
    # protocol buffers, these correspond to nested messages and repeated
    # fields, respectively.
    proto_rows = types.ProtoRows()

    row = sample_data_pb2.SampleData()
    row.row_num = 13
    row.int64_list.append(1)
    row.int64_list.append(2)
    row.int64_list.append(3)
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 14
    row.struct_col.sub_int_col = 7
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 15
    sub_message = sample_data_pb2.SampleData.SampleStruct()
    sub_message.sub_int_col = -1
    row.struct_list.append(sub_message)
    sub_message = sample_data_pb2.SampleData.SampleStruct()
    sub_message.sub_int_col = -2
    row.struct_list.append(sub_message)
    sub_message = sample_data_pb2.SampleData.SampleStruct()
    sub_message.sub_int_col = -3
    row.struct_list.append(sub_message)
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 16
    date_value = datetime.date(2021, 8, 8)
    epoch_value = datetime.date(1970, 1, 1)
    delta = date_value - epoch_value
    row.range_date.start = delta.days
    proto_rows.serialized_rows.append(row.SerializeToString())

    request = types.AppendRowsRequest()
    request.offset = 12
    proto_data = types.AppendRowsRequest.ProtoData()
    proto_data.rows = proto_rows
    request.proto_rows = proto_data

    # For each request sent, a message is expected in the responses iterable.
    # This sample sends 3 requests, therefore expect exactly 3 responses.
    response_future_3 = append_rows_stream.send(request)

    # All three requests are in-flight, wait for them to finish being processed
    # before finalizing the stream.
    print(response_future_1.result())
    print(response_future_2.result())
    print(response_future_3.result())

    # Shutdown background threads and close the streaming connection.
    append_rows_stream.close()

    # A PENDING type stream must be "finalized" before being committed. No new
    # records can be written to the stream after this method has been called.
    write_client.finalize_write_stream(name=write_stream.name)

    # Commit the stream you created earlier.
    batch_commit_write_streams_request = types.BatchCommitWriteStreamsRequest()
    batch_commit_write_streams_request.parent = parent
    batch_commit_write_streams_request.write_streams = [write_stream.name]
    write_client.batch_commit_write_streams(batch_commit_write_streams_request)

    print(f"Writes to stream: '{write_stream.name}' have been committed.")


# [END bigquerystorage_append_rows_raw_proto2]
