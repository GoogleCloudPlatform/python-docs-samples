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

# DO NOT EDIT! This is a generated sample ("RequestPagedAll",  "automl_video_object_tracking_list_models")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-automl

# sample-metadata
#   title: List Models
#   description: List Models
#   usage: python3 samples/v1beta1/automl_video_object_tracking_list_models.py [--filter "video_object_tracking_model_metadata:*"] [--project "[Google Cloud Project ID]"]
import sys

# [START automl_video_object_tracking_list_models]

from google.cloud import automl_v1beta1


def sample_list_models(filter_, project):
    """
    List Models

    Args:
      filter_ An expression for filtering the results of the request.
      This filters for Models which have video_object_tracking_model_metadata.
      project Required. Your Google Cloud Project ID.
    """

    client = automl_v1beta1.AutoMlClient()

    # filter_ = 'video_object_tracking_model_metadata:*'
    # project = '[Google Cloud Project ID]'
    parent = client.location_path(project, "us-central1")

    # Iterate over all results
    for response_item in client.list_models(parent, filter_=filter_):
        model = response_item
        print(u"Model name: {}".format(model.name))
        print(u"Display name: {}".format(model.display_name))
        print(u"Dataset ID: {}".format(model.dataset_id))
        print(u"Create time: {}".format(model.create_time))
        print(u"Update time: {}".format(model.update_time))


# [END automl_video_object_tracking_list_models]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filter", type=str, default="video_object_tracking_model_metadata:*"
    )
    parser.add_argument("--project", type=str, default="[Google Cloud Project ID]")
    args = parser.parse_args()

    sample_list_models(args.filter, args.project)


if __name__ == "__main__":
    main()
