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
#   title: Get Long-Running Operation Status
#   description: Get Long-Running Operation Status
#   usage: python3 samples/v1beta1/automl_get_operation.py [--project "[Google Cloud Project ID]"] [--operation_id "[Operation ID]"]
import sys

# [START automl_get_operation]

from google.cloud import automl_v1beta1


def sample_get_operation(project, operation_id):
    """
    Get Long-Running Operation Status

    Args:
      project Required. Your Google Cloud Project ID.
      operation_id Required. The ID of the Operation.
    """

    client = automl_v1beta1.AutoMlClient()

    operations_client = client.transport._operations_client

    # project = '[Google Cloud Project ID]'
    # operation_id = '[Operation ID]'
    name = "projects/{}/locations/us-central1/operations/{}".format(
        project, operation_id
    )

    operation = operations_client.get_operation(name)

    # Print Operation status and info
    print(u"Operation Name: {}".format(operation.name))
    print(u"Done: {}".format(operation.done))
    print(u"Response: {}".format(operation.response))
    print(u"Metadata: {}".format(operation.metadata))


# [END automl_get_operation]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, default="[Google Cloud Project ID]")
    parser.add_argument("--operation_id", type=str, default="[Operation ID]")
    args = parser.parse_args()

    sample_get_operation(args.project, args.operation_id)


if __name__ == "__main__":
    main()
