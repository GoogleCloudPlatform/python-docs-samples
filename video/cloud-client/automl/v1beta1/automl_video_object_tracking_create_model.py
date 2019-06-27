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

# DO NOT EDIT! This is a generated sample ("LongRunningStartThenCancel",  "automl_video_object_tracking_create_model")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-automl

# sample-metadata
#   title: Create Model
#   description: Create a model
#   usage: python3 samples/v1beta1/automl_video_object_tracking_create_model.py [--display_name "My_Model_Name_123"] [--dataset_id "[Dataset ID]"] [--project "[Google Cloud Project ID]"]
import sys

# [START automl_video_object_tracking_create_model]

from google.cloud import automl_v1beta1


def sample_create_model(display_name, dataset_id, project):
    """
    Create a model

    Args:
      display_name The name of the model to show in the interface.
      The name can be up to 32 characters long and can consist only of
      ASCII Latin letters A-Z and a-z, underscores (_), and ASCII digits 0-9.
      Must be unique within the scope of the provided GCP Project and Location.
      dataset_id Required. The resource ID of the dataset used to create the model.
      The dataset must come from the same ancestor project and location.
      project Required. Your Google Cloud Project ID.
    """

    client = automl_v1beta1.AutoMlClient()

    # display_name = 'My_Model_Name_123'
    # dataset_id = '[Dataset ID]'
    # project = '[Google Cloud Project ID]'
    parent = client.location_path(project, "us-central1")

    # Initialized video_object_tracking_model_metadata field must be provided.
    # This specifies this Dataset is to be used for video object tracking.
    video_object_tracking_model_metadata = {}
    model = {
        "display_name": display_name,
        "dataset_id": dataset_id,
        "video_object_tracking_model_metadata": video_object_tracking_model_metadata,
    }

    operation = client.create_model(parent, model).operation

    # The long-running operation to create model has started.
    # Store the operation name for operation status polling
    print(u"Started long-running operation: {}".format(operation.name))


# [END automl_video_object_tracking_create_model]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--display_name", type=str, default="My_Model_Name_123")
    parser.add_argument("--dataset_id", type=str, default="[Dataset ID]")
    parser.add_argument("--project", type=str, default="[Google Cloud Project ID]")
    args = parser.parse_args()

    sample_create_model(args.display_name, args.dataset_id, args.project)


if __name__ == "__main__":
    main()
