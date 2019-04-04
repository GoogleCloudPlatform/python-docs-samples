#!/usr/bin/env python

# Copyright 2019 Google LLC
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

import argparse
import os

def predict(project_id, compute_region, model_id, file_path):
    """Detect the content entity label."""
    # [START automl_natural_language_predict]
    # TODO(developer): Uncomment and set the following variables
    # project_id = '[PROJECT_ID]'
    # compute_region = '[COMPUTE_REGION]'
    # model_id = '[MODEL_ID]'
    # file_path = '/local/path/to/file'

    from google.cloud import automl_v1beta1 as automl

    automl_client = automl.AutoMlClient()

    # Create client for prediction service.
    prediction_client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = automl_client.model_path(
        project_id, compute_region, model_id
    )

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
        print("Predicted entity label: {}".format(result.display_name))
        print("Predicted confidence score: {}".format(result.text_extraction.score))
        print("Predicted text segment: {}".format(result.text_extraction.text_segment.content))
        print("Predicted text segment start offset: {}".format(result.text_extraction.text_segment.start_offset))
        print("Predicted text segment end offset : {}".format(result.text_extraction.text_segment.end_offset))
        print("\n")

    # [END automl_natural_language_predict]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
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
