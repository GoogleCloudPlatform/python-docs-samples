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

# DO NOT EDIT! This is a generated sample ("Request",  "automl_video_object_tracking_create_dataset")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-automl

# sample-metadata
#   title: Create Dataset
#   description: Create Dataset
#   usage: python3 samples/v1beta1/automl_video_object_tracking_create_dataset.py [--display_name "My_Dataset_Name_123"] [--project "[Google Cloud Project ID]"]
import sys

# [START automl_video_object_tracking_create_dataset]

from google.cloud import automl_v1beta1


def sample_create_dataset(display_name, project):
    """
    Create Dataset

    Args:
      display_name The name of the dataset to show in the interface.
      The name can be up to 32 characters long and can consist only of
      ASCII Latin letters A-Z and a-z, underscores (_), and ASCII digits 0-9.
      Must be unique within the scope of the provided GCP Project and Location.
      project Required. Your Google Cloud Project ID.
    """

    client = automl_v1beta1.AutoMlClient()

    # display_name = 'My_Dataset_Name_123'
    # project = '[Google Cloud Project ID]'
    parent = client.location_path(project, "us-central1")

    # User-provided description of dataset (optional)
    description = "Description of this dataset"

    # Initialized video_object_tracking_dataset_metadata field must be provided.
    # This specifies this Dataset is to be used for video object tracking.
    video_object_tracking_dataset_metadata = {}
    dataset = {
        "display_name": display_name,
        "description": description,
        "video_object_tracking_dataset_metadata": video_object_tracking_dataset_metadata,
    }

    response = client.create_dataset(parent, dataset)
    print(u"Created Dataset.")
    dataset = response
    # Print out the full name of the created dataset.
    #
    # This will have the format:
    #   projects/[Google Cloud Project Number]/locations/us-central1/datasets/VOT1234567890123456789
    #
    print(u"Name: {}".format(dataset.name))
    # Print out the Display Name (the text you provided during creation)
    print(u"Display Name: {}".format(dataset.display_name))
    # Print out the user-provided description (may be blank)
    print(u"Description: {}".format(dataset.description))
    # The number of examples in the dataset, if any.
    # Added by importing data via import_data
    #
    print(u"Example count: {}".format(dataset.example_count))


# [END automl_video_object_tracking_create_dataset]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--display_name", type=str, default="My_Dataset_Name_123")
    parser.add_argument("--project", type=str, default="[Google Cloud Project ID]")
    args = parser.parse_args()

    sample_create_dataset(args.display_name, args.project)


if __name__ == "__main__":
    main()
