#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations on prediction
with the Google AutoML Natural Language API.

For more information, see the tutorial page at
https://cloud.google.com/natural-language/automl/docs/
"""

# [START automl_natural_language_import]
import argparse
import os

from google.cloud import automl_v1beta1 as automl

# [END automl_natural_language_import]


# [START automl_natural_language_predict]
def predict(project_id, compute_region, model_id, file_path):
    """Classify the content.
    Args:
        project_id: Id of the project.
        compute_region: Region name.
        model_id: Id of the model which will be used for text classification.
        file_path: Local text file path of the content to be classified.
    """
    automl_client = automl.AutoMlClient()

    # Create client for prediction service.
    prediction_client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = automl_client.model_path(project_id, compute_region, model_id)

    # Read the file content for prediction.
    with open(file_path, "rb") as content_file:
        snippet = content_file.read()

    # Set the payload by giving the content and type of the file.
    payload = {"text_snippet": {"content": snippet, "mime_type": "text/plain"}}

    # params is additional domain-specific parameters.
    # currently there is no additional parameters supported.
    params = {}
    response = prediction_client.predict(model_full_id, payload, params)
    print("Prediction results:")
    for result in response.payload:
        print("Predicted class name: {}".format(result.display_name))
        print("Predicted class score: {}".format(result.classification.score))


# [END automl_natural_language_predict]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command")

    predict_parser = subparsers.add_parser("predict", help=predict.__doc__)
    predict_parser.add_argument("model_id")
    predict_parser.add_argument("file_path")

    project_id = os.environ["PROJECT_ID"]
    compute_region = os.environ["REGION_NAME"]

    args = parser.parse_args()

    if args.command == "predict":
        predict(project_id, compute_region, args.model_id, args.file_path)
