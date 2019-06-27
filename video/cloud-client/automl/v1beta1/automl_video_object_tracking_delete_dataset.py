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

# DO NOT EDIT! This is a generated sample ("LongRunningPromise",  "automl_video_object_tracking_delete_dataset")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-automl

# sample-metadata
#   title: Delete Dataset
#   description: Delete Dataset
#   usage: python3 samples/v1beta1/automl_video_object_tracking_delete_dataset.py [--dataset_id "[Dataset ID]"] [--project "[Google Cloud Project ID]"]
import sys

# [START automl_video_object_tracking_delete_dataset]

from google.cloud import automl_v1beta1


def sample_delete_dataset(dataset_id, project):
    """
    Delete Dataset

    Args:
      dataset_id Dataset ID
      project Required. Your Google Cloud Project ID.
    """

    client = automl_v1beta1.AutoMlClient()

    # dataset_id = '[Dataset ID]'
    # project = '[Google Cloud Project ID]'
    name = client.dataset_path(project, "us-central1", dataset_id)

    operation = client.delete_dataset(name)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    print(u"Deleted Dataset.")


# [END automl_video_object_tracking_delete_dataset]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_id", type=str, default="[Dataset ID]")
    parser.add_argument("--project", type=str, default="[Google Cloud Project ID]")
    args = parser.parse_args()

    sample_delete_dataset(args.dataset_id, args.project)


if __name__ == "__main__":
    main()
