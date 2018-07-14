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
with the Google AutoML Translation API.

For more information, see the documentation at
https://cloud.google.com/translate/automl/docs
"""

# [START automl_translation_import]
import argparse
import os

from google.cloud import automl_v1beta1 as automl
# [END automl_translation_import]


# [START automl_translation_predict]
def predict(
        project_id, compute_region, model_id, file_path,
        translation_allow_fallback=False):
    """Translate the content.
    Args:
        project_id: Id of the project.
        compute_region: Region name.
        model_id: Id of the model which translation needs to use.
        file_path: Input file path of the content to be translated.
        translation_allow_fallback: Use true if AutoML will fall-back
            to use a Google translation model for translation requests
            if the specified AutoML translation model cannot serve the request.
            Use false to not use Google translation model.
    """
    automl_client = automl.AutoMlClient()

    # Create client for prediction service.
    prediction_client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = automl_client.model_path(
        project_id, compute_region, model_id)

    # Read the file content for translation.
    with open(file_path, 'rb') as content_file:
        content = content_file.read()
    content.decode('utf-8')

    # Set the payload by giving the content of the file.
    payload = {
        'text_snippet': {
            'content': content
        }
    }

    # params is additional domain-specific parameters.
    # translation_allow_fallback allows to use Google translation model.
    params = {}
    if(translation_allow_fallback):
        params = {'translation_allow_fallback': 'True'}

    response = prediction_client.predict(model_full_id, payload, params)
    translated_content = response.payload[0].translation.translated_content

    print(u'Translated content: {}'.format(translated_content.content))
# [END automl_translation_predict]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    predict_parser = subparsers.add_parser(
        'predict', help=predict.__doc__)
    predict_parser.add_argument('model_id')
    predict_parser.add_argument('file_path')
    predict_parser.add_argument(
        'translation_allow_fallback', nargs='?', choices=['False', 'True'],
        default='False')

    project_id = os.environ['PROJECT_ID']
    compute_region = os.environ['REGION_NAME']

    args = parser.parse_args()

    if args.command == 'predict':
        translation_allow_fallback = (
            True if args.translation_allow_fallback == 'True' else False)
        predict(
            project_id, compute_region, args.model_id, args.file_path,
            translation_allow_fallback)
