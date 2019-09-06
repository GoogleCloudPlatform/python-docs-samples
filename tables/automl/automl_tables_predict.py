#!/usr/bin/env python

# Copyright 2019 Google LLC
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

"""This application demonstrates how to perform basic operations on prediction
with the Google AutoML Tables API.

For more information, the documentation at
https://cloud.google.com/automl-tables/docs.
"""

import argparse
import os


def predict(project_id,
            compute_region,
            model_display_name,
            inputs):
    """Make a prediction."""
    # [START automl_tables_predict]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_display_name = 'MODEL_DISPLAY_NAME_HERE'
    # inputs = {'value': 3, ...}

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    response = client.predict(
        model_display_name=model_display_name,
        inputs=inputs)
    print("Prediction results:")
    for result in response.payload:
        print("Predicted class name: {}".format(result.display_name))
        print("Predicted class score: {}".format(
            result.classification.score))

    # [END automl_tables_predict]


def batch_predict(project_id,
                  compute_region,
                  model_display_name,
                  gcs_input_uris,
                  gcs_output_uri):
    """Make a batch of predictions."""
    # [START automl_tables_batch_predict]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_display_name = 'MODEL_DISPLAY_NAME_HERE'
    # gcs_input_uris = ['gs://path/to/file.csv]
    # gcs_output_uri = 'gs://path'

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    # Query model
    response = client.batch_predict(
        gcs_input_uris, gcs_output_uri, model_display_name=model_display_name
    )
    print("Making batch prediction... ")
    response.result()
    print("Batch prediction complete.\n{}".format(response.metadata))

    # [END automl_tables_batch_predict]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    predict_parser = subparsers.add_parser("predict", help=predict.__doc__)
    predict_parser.add_argument("--model_display_name")
    predict_parser.add_argument("--file_path")

    batch_predict_parser = subparsers.add_parser(
        "batch_predict", help=predict.__doc__
    )
    batch_predict_parser.add_argument("--model_display_name")
    batch_predict_parser.add_argument("--input_path")
    batch_predict_parser.add_argument("--output_path")

    project_id = os.environ["PROJECT_ID"]
    compute_region = os.environ["REGION_NAME"]

    args = parser.parse_args()

    if args.command == "predict":
        predict(
            project_id,
            compute_region,
            args.model_display_name,
            args.file_path,
        )

    if args.command == "batch_predict":
        batch_predict(
            project_id,
            compute_region,
            args.model_display_name,
            args.input_path,
            args.output_path,
        )
