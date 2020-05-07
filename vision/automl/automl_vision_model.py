#!/usr/bin/env python

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations on model
with the Google AutoML Vision API.

For more information, the documentation at
https://cloud.google.com/vision/automl/docs.
"""

import argparse
import os


def create_model(
    project_id, compute_region, dataset_id, model_name, train_budget=24
):
    """Create a model."""
    # [START automl_vision_create_model]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # dataset_id = 'DATASET_ID_HERE'
    # model_name = 'MODEL_NAME_HERE'
    # train_budget = integer amount for maximum cost of model

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform location.
    project_location = client.location_path(project_id, compute_region)

    # Set model name and model metadata for the image dataset.
    my_model = {
        "display_name": model_name,
        "dataset_id": dataset_id,
        "image_classification_model_metadata": {"train_budget": train_budget}
        if train_budget
        else {},
    }

    # Create a model with the model metadata in the region.
    response = client.create_model(project_location, my_model)

    print("Training operation name: {}".format(response.operation.name))
    print("Training started...")

    # [END automl_vision_create_model]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    create_model_parser = subparsers.add_parser(
        "create_model", help=create_model.__doc__
    )
    create_model_parser.add_argument("dataset_id")
    create_model_parser.add_argument("model_name")
    create_model_parser.add_argument(
        "train_budget", type=int, nargs="?", default=0
    )

    project_id = os.environ["PROJECT_ID"]
    compute_region = os.environ["REGION_NAME"]

    args = parser.parse_args()

    if args.command == "create_model":
        create_model(
            project_id,
            compute_region,
            args.dataset_id,
            args.model_name,
            args.train_budget,
        )
