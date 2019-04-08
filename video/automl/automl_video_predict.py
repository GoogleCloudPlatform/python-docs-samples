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

"""This application demonstrates how to perform basic operations on dataset
with the Google AutoML Video API.

For more information, the documentation at
https://cloud.google.com/video-intelligence/automl/docs/.
"""

import argparse
import os


def batch_predict(
    project_id, compute_region, model_id, input_uri, output_uri_prefix):
    """Make a batch of predictions."""
    # [START automl_video_batch_predict]
    # TODO(developer): Uncomment and set the following variables
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_id = 'MODEL_ID_HERE'
    # input_uri = 'gs://path/to/file.csv'
    # output_uri_prefix = 'gs://path'


    from google.cloud import automl_v1beta1 as automl
    import csv

    automl_client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = automl_client.model_path(
        project_id, compute_region, model_id
    )

    # Create client for prediction service.
    prediction_client = automl.PredictionServiceClient()

    # Input configuration.
    input_config = dict(gcs_source={'input_uris': [input_uri]})

    # Output configuration.
    output_config = dict(
        gcs_destination={'output_uri_prefix': output_uri_prefix}
    )

    # Launch long-running batch prediction operation.
    response = prediction_client.batch_predict(model_full_id, input_config,
                                                output_config)
    print("Making batch prediction... ")
    try:
        result = response.result()
    except:
        # Hides Any to BatchPredictResult error.
        pass
    print("Batch prediction complete.\n{}".format(response.metadata))

    # [END automl_video_batch_predict]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    batch_predict_parser = subparsers.add_parser(
        "batch_predict", help=batch_predict.__doc__
    )
    batch_predict_parser.add_argument("--model_id")
    batch_predict_parser.add_argument("--input_uri")
    batch_predict_parser.add_argument("--output_uri_prefix")

    project_id = os.environ["PROJECT_ID"]
    compute_region = os.environ["REGION_NAME"]

    args = parser.parse_args()

    if args.command == "batch_predict":
        batch_predict(
            project_id,
            compute_region,
            args.model_id,
            args.input_uri,
            args.output_uri_prefix,
        )
