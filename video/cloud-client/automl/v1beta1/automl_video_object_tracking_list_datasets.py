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

# DO NOT EDIT! This is a generated sample ("RequestPagedAll",  "automl_video_object_tracking_list_datasets")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-automl

# sample-metadata
#   title: List Datasets
#   description: List Datasets
#   usage: python3 samples/v1beta1/automl_video_object_tracking_list_datasets.py [--project "[Google Cloud Project ID]"]
import sys

# [START automl_video_object_tracking_list_datasets]

from google.cloud import automl_v1beta1


def sample_list_datasets(project):
    """
    List Datasets

    Args:
      project Required. Your Google Cloud Project ID.
    """

    client = automl_v1beta1.AutoMlClient()

    # project = '[Google Cloud Project ID]'
    parent = client.location_path(project, "us-central1")

    # An expression for filtering the results of the request.
    # This filters for Datasets which have video_object_tracking_dataset_metadata.
    filter_ = "video_object_tracking_dataset_metadata:*"

    # Iterate over all results
    for response_item in client.list_datasets(parent, filter_=filter_):
        dataset = response_item
        print(u"Name: {}".format(dataset.name))
        print(u"Display Name: {}".format(dataset.display_name))
        print(u"Description: {}".format(dataset.description))
        # The number of examples in the dataset, if any.
        # Added by importing data via import_data
        #
        print(u"Example count: {}".format(dataset.example_count))


# [END automl_video_object_tracking_list_datasets]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, default="[Google Cloud Project ID]")
    args = parser.parse_args()

    sample_list_datasets(args.project)


if __name__ == "__main__":
    main()
