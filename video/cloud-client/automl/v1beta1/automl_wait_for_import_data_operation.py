# -*- coding: utf-8 -*-
#
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

# This sample is HAND-WRITTEN

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-automl

# sample-metadata
#   title: Wait for import data to complete
#   description: Wait for import data to complete
#   usage: python3 samples/v1beta1/automl_wait_for_import_data_operation.py [--project "[Google Cloud Project ID]"] [--operation_id "[Operation ID]"]
import sys

# [START automl_wait_for_import_data_operation]

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import operations_pb2 as proto_operations_pb2
from google.protobuf import empty_pb2
import google.api_core


def sample_wait_for_import_data_operation(project, operation_id, timeout):
    """
    Wait for import data to complete

    Args:
      project Required. Your Google Cloud Project ID.
      operation_id Required. The ID of the Operation.
      timeout Seconds to wait for operation before timeout. Defaults 5 minutes.
    """

    client = automl_v1beta1.AutoMlClient()

    operations_client = client.transport._operations_client

    # project = '[Google Cloud Project ID]'
    # operation_id = '[Operation ID]'
    # timeout = 300
    name = "projects/{}/locations/us-central1/operations/{}".format(
        project, operation_id
    )

    api_operation = operations_client.get_operation(name)

    # Specify the types that this long-running operation returns (from API Reference)
    operation_return_type = empty_pb2.Empty
    operation_metadata_type = proto_operations_pb2.OperationMetadata

    # Create `Operation` object which has methods including result() which
    # polls and waits for the long-running operation to complete.
    #
    # `Operation` object has other useful methods: cancel(), done(), cancelled()
    #
    # You must specify the type of proto object which this operation returns,
    # in this case we are waiting for a Model returned by CreateModel.
    operation = google.api_core.operation.from_gapic(
        api_operation,
        operations_client,
        operation_return_type,
        metadata_type=operation_metadata_type,
    )

    try:
        print(u"Waiting for operation...")
        result = operation.result()

        print(u"Operation finished.")
        print(result)

    except google.api_core.exceptions.GoogleAPICallError as api_error:
        print(u"API Error: {}".format(api_error.message))


# [END automl_wait_for_import_data_operation]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, default="[Google Cloud Project ID]")
    parser.add_argument("--operation_id", type=str, default="[Operation ID]")
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    sample_wait_for_import_data_operation(args.project, args.operation_id, args.timeout)


if __name__ == "__main__":
    main()
