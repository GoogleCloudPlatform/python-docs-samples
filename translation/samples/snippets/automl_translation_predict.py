#!/usr/bin/env python

# Copyright 2018 Google LLC
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
with the Google AutoML Translation API.

For more information, see the documentation at
https://cloud.google.com/translate/automl/docs
"""

import argparse
import os


def predict(project_id, compute_region, model_id, file_path):
    """Translate the content."""
    # [START automl_translate_predict]
    # project_id = 'PROJECT_ID_HERE'
    # compute_region = 'COMPUTE_REGION_HERE'
    # model_id = 'MODEL_ID_HERE'
    # file_path = '/local/path/to/file'

    from google.cloud import automl_v1beta1 as automl

    automl_client = automl.AutoMlClient()

    # Create client for prediction service.
    prediction_client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = automl_client.model_path(
        project_id, compute_region, model_id
    )

    # Read the file content for translation.
    with open(file_path, "rb") as content_file:
        content = content_file.read()
    content.decode("utf-8")

    # Set the payload by giving the content of the file.
    payload = {"text_snippet": {"content": content}}

    # params is additional domain-specific parameters.
    params = {}

    response = prediction_client.predict(model_full_id, payload, params)
    translated_content = response.payload[0].translation.translated_content

    print(u"Translated content: {}".format(translated_content.content))

    # [END automl_translate_predict]


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
