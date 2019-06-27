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
#   title: List Long-Running Operations
#   description: List Long-Running Operations
#   usage: python3 samples/v1beta1/automl_list_operations.py [--project "[Google Cloud Project ID]"] [--filter ""]
import sys

# [START automl_list_operations]

from google.cloud import automl_v1beta1


def sample_list_operations(project, filter_):
    """
    List Long-Running Operations

    Args:
      project Required. Your Google Cloud Project ID.
      filter_ Filter operations
    """

    client = automl_v1beta1.AutoMlClient()

    operations_client = client.transport._operations_client

    # project = '[Google Cloud Project ID]'
    name = client.location_path(project, "us-central1")

    # Iterate over all results
    for response_item in operations_client.list_operations(name, filter_=filter_):
        operation = response_item
        print(u"Operation Name: {}".format(operation.name))
        print(u"Done: {}".format(operation.done))
        print(u"Response: {}".format(operation.response))
        print(u"Metadata: {}".format(operation.metadata))


# [END automl_list_operations]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, default="[Google Cloud Project ID]")
    parser.add_argument("--filter", type=str, default="")
    args = parser.parse_args()

    sample_list_operations(args.project, args.filter)


if __name__ == "__main__":
    main()
