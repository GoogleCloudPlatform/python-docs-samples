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

# DO NOT EDIT! This is a generated sample ("LongRunningPromise",  "automl_video_object_tracking_import_data")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-automl

# sample-metadata
#   title: Import Data
#   description: Import training data into dataset
#   usage: python3 samples/v1beta1/automl_video_object_tracking_import_data.py [--dataset_id "[Dataset ID]"] [--project "[Google Cloud Project ID]"]
import sys

# [START automl_video_object_tracking_import_data]

from google.cloud import automl_v1beta1


def sample_import_data(dataset_id, project):
    """
    Import training data into dataset

    Args:
      dataset_id Dataset ID, e.g. VOT1234567890123456789
      project Required. Your Google Cloud Project ID.
    """

    client = automl_v1beta1.AutoMlClient()

    # dataset_id = '[Dataset ID]'
    # project = '[Google Cloud Project ID]'
    name = client.dataset_path(project, "us-central1", dataset_id)

    # Paths to CSV files stored in Cloud Storage with training data.
    # See "Preparing your training data" for more information.
    # https://cloud.google.com/video-intelligence/automl/object-tracking/docs/prepare
    input_uris_element = "gs://automl-video-datasets/youtube_8m_videos_animal_tiny.csv"
    input_uris = [input_uris_element]
    gcs_source = {"input_uris": input_uris}
    input_config = {"gcs_source": gcs_source}

    operation = client.import_data(name, input_config)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    print(u"Imported training data.")


# [END automl_video_object_tracking_import_data]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_id", type=str, default="[Dataset ID]")
    parser.add_argument("--project", type=str, default="[Google Cloud Project ID]")
    args = parser.parse_args()

    sample_import_data(args.dataset_id, args.project)


if __name__ == "__main__":
    main()
