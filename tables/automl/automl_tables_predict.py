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
            model_id,
            file_path,
            score_threshold="",
):
    """Make a prediction."""
    # [START automl_tables_predict]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_id = 'MODEL_ID_HERE'
    # file_path = '/local/path/to/file'
    # score_threshold = 'value from 0.0 to 0.5'

    from google.cloud import automl_v1beta1 as automl
    import csv

    automl_client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = automl_client.model_path(
        project_id, compute_region, model_id
    )

    # Create client for prediction service.
    prediction_client = automl.PredictionServiceClient()

    # params is additional domain-specific parameters.
    # score_threshold is used to filter the result
    # Initialize params
    params = {}
    if score_threshold:
        params = {"score_threshold": score_threshold}

    with open(file_path, "rt") as csv_file:
        # Read each row of csv
        content = csv.reader(csv_file)
        for row in content:
            # Create payload
            values = []
            for column in row:
                values.append({'number_value': float(column)})
            payload = {
                'row': {'values': values}
            }

            # Query model
            response = prediction_client.predict(model_full_id, payload)
            print("Prediction results:")
            for result in response.payload:
                print("Predicted class name: {}".format(result.display_name))
                print("Predicted class score: {}".format(result.classification.score))

    # [END automl_tables_predict]


def batch_predict(project_id,
                  compute_region,
                  model_id,
                  input_path,
                  output_path):
    """Make a batch of predictions."""
    # [START automl_tables_batch_predict]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_id = 'MODEL_ID_HERE'
    # input_path = 'gs://path/to/file.csv' or
    #   'bq://project_id.dataset_id.table_id'
    # output_path = 'gs://path' or `bq://project_id'


    from google.cloud import automl_v1beta1 as automl
    import csv

    automl_client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = automl_client.model_path(
        project_id, compute_region, model_id
    )

    # Create client for prediction service.
    prediction_client = automl.PredictionServiceClient()

    if input_path.startswith('bq'):
        input_config = {"bigquery_source": {"input_uri": input_path}}
    else:    
        # Get the multiple Google Cloud Storage URIs.
        input_uris = input_path.split(",").strip()
        input_config = {"gcs_source": {"input_uris": input_uris}}

    if output_path.startswith('bq'):
        output_config = {"bigquery_destination": {"output_uri": output_path}}
    else:    
        # Get the multiple Google Cloud Storage URIs.
        output_uris = output_path.split(",").strip()
        output_config = {"gcs_destination": {"output_uris": output_uris}}

    # Query model
    response = prediction_client.batch_predict(
        model_full_id, input_config, output_config)
    print("Making batch prediction... ")
    try:
        result = response.result()
    except:
        # Hides Any to BatchPredictResult error.
        pass
    print("Batch prediction complete.\n{}".format(response.metadata))

    # [END automl_tables_batch_predict]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    predict_parser = subparsers.add_parser("predict", help=predict.__doc__)
    predict_parser.add_argument("--model_id")
    predict_parser.add_argument("--file_path")
    predict_parser.add_argument("--score_threshold", nargs="?", default="")

    batch_predict_parser = subparsers.add_parser(
        "batch_predict", help=predict.__doc__
    )
    batch_predict_parser.add_argument("--model_id")
    batch_predict_parser.add_argument("--input_path")
    batch_predict_parser.add_argument("--output_path")

    project_id = os.environ["PROJECT_ID"]
    compute_region = os.environ["REGION_NAME"]

    args = parser.parse_args()

    if args.command == "predict":
        predict(
            project_id,
            compute_region,
            args.model_id,
            args.file_path,
            args.score_threshold,
        )

    if args.command == "batch_predict":
        batch_predict(
            project_id,
            compute_region,
            args.model_id,
            args.input_path,
            args.output_path,
        )