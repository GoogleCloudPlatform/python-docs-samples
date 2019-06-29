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

# DO NOT EDIT! This is a generated sample ("Request",  "automl_video_object_tracking_get_model")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-automl

# sample-metadata
#   title: Get Model
#   description: Get model and print model details
#   usage: python3 samples/v1beta1/automl_video_object_tracking_get_model.py [--model_id "[Model ID]"] [--project "[Google Cloud Project ID]"]
import sys

# [START automl_video_object_tracking_get_model]

from google.cloud import automl_v1beta1


def sample_get_model(model_id, project):
    """
    Get model and print model details

    Args:
      model_id Model ID, e.g. VOT1234567890123456789
      project Required. Your Google Cloud Project ID.
    """

    client = automl_v1beta1.AutoMlClient()

    # model_id = '[Model ID]'
    # project = '[Google Cloud Project ID]'
    name = client.model_path(project, "us-central1", model_id)

    response = client.get_model(name)
    model = response
    # Print out the full name of the created model.
    #
    # This will have the format:
    #   projects/[Google Cloud Project Number]/locations/us-central1/models/VOT1234567890123456789
    #
    # The Model ID is the generated identifer in this path, e.g. VOT1234567890123456789
    # You will need this ID to perform operations on the model including predictions.
    #
    print(u"Model name: {}".format(model.name))
    # Print out the Display Name (the text you provided during creation)
    print(u"Display name: {}".format(model.display_name))
    # Print out the ID of the dataset used to create this model.
    #
    # Note: this is the Dataset ID, e.g. VOT1234567890123456789
    #
    print(u"Dataset ID: {}".format(model.dataset_id))
    print(u"Create time: {}".format(model.create_time))
    print(u"Update time: {}".format(model.update_time))


# [END automl_video_object_tracking_get_model]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model_id", type=str, default="[Model ID]")
    parser.add_argument("--project", type=str, default="[Google Cloud Project ID]")
    args = parser.parse_args()

    sample_get_model(args.model_id, args.project)


if __name__ == "__main__":
    main()
