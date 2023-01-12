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


def predict(
    project_id,
    compute_region,
    model_display_name,
    inputs,
    feature_importance=None,
):
    """Make a prediction."""
    # [START automl_tables_predict]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_display_name = 'MODEL_DISPLAY_NAME_HERE'
    # inputs = {'value': 3, ...}

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    if feature_importance:
        response = client.predict(
            model_display_name=model_display_name,
            inputs=inputs,
            feature_importance=True,
        )
    else:
        response = client.predict(
            model_display_name=model_display_name, inputs=inputs
        )

    print("Prediction results:")
    for result in response.payload:
        print(
            "Predicted class name: {}".format(result.tables.value)
        )
        print("Predicted class score: {}".format(result.tables.score))

        if feature_importance:
            # get features of top importance
            feat_list = [
                (column.feature_importance, column.column_display_name)
                for column in result.tables.tables_model_column_info
            ]
            feat_list.sort(reverse=True)
            if len(feat_list) < 10:
                feat_to_show = len(feat_list)
            else:
                feat_to_show = 10

            print("Features of top importance:")
            for feat in feat_list[:feat_to_show]:
                print(feat)

    # [END automl_tables_predict]


def batch_predict_bq(
    project_id,
    compute_region,
    model_display_name,
    bq_input_uri,
    bq_output_uri,
    params
):
    """Make a batch of predictions."""
    # [START automl_tables_batch_predict_bq]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_display_name = 'MODEL_DISPLAY_NAME_HERE'
    # bq_input_uri = 'bq://my-project.my-dataset.my-table'
    # bq_output_uri = 'bq://my-project'
    # params = {}

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    # Query model
    response = client.batch_predict(bigquery_input_uri=bq_input_uri,
                                    bigquery_output_uri=bq_output_uri,
                                    model_display_name=model_display_name,
                                    params=params)
    print("Making batch prediction... ")
    # `response` is a async operation descriptor,
    # you can register a callback for the operation to complete via `add_done_callback`:
    # def callback(operation_future):
    #   result = operation_future.result()
    # response.add_done_callback(callback)
    #
    # or block the thread polling for the operation's results:
    response.result()
    # AutoML puts predictions in a newly generated dataset with a name by a mask "prediction_" + model_id + "_" + timestamp
    # here's how to get the dataset name:
    dataset_name = response.metadata.batch_predict_details.output_info.bigquery_output_dataset

    print("Batch prediction complete.\nResults are in '{}' dataset.\n{}".format(
        dataset_name, response.metadata))

    # [END automl_tables_batch_predict_bq]


def batch_predict(
    project_id,
    compute_region,
    model_display_name,
    gcs_input_uri,
    gcs_output_uri,
    params,
):
    """Make a batch of predictions."""
    # [START automl_tables_batch_predict]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_display_name = 'MODEL_DISPLAY_NAME_HERE'
    # gcs_input_uri = 'gs://YOUR_BUCKET_ID/path_to_your_input_csv'
    # gcs_output_uri = 'gs://YOUR_BUCKET_ID/path_to_save_results/'
    # params = {}

    from google.cloud import automl_v1beta1 as automl

    client = automl.TablesClient(project=project_id, region=compute_region)

    # Query model
    response = client.batch_predict(
        gcs_input_uris=gcs_input_uri,
        gcs_output_uri_prefix=gcs_output_uri,
        model_display_name=model_display_name,
        params=params
    )
    print("Making batch prediction... ")
    # `response` is a async operation descriptor,
    # you can register a callback for the operation to complete via `add_done_callback`:
    # def callback(operation_future):
    #   result = operation_future.result()
    # response.add_done_callback(callback)
    #
    # or block the thread polling for the operation's results:
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
            project_id, compute_region, args.model_display_name, args.file_path
        )

    if args.command == "batch_predict":
        batch_predict(
            project_id,
            compute_region,
            args.model_display_name,
            args.input_path,
            args.output_path,
        )
