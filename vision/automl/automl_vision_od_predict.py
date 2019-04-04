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
"""This application demonstrates how to perform basic operations on

object detection datasets with the Google AutoML API.  For more information, the
documentation at
https://cloud.google.com/vision/automl/docs.
"""
from __future__ import print_function

import argparse
import os

def predict(project_id, compute_region, model_id, local_image_path):
  """Online prediciton for a single local image."""
  # [START automl_vision_iod_predict]
  ## To do: Uncomment and set the following variables
  # project_id = '[PROJECT_ID]'
  # compute_region = '[COMPUTE_REGION]'
  # model_id = '[MODEL_ID]'
  # local_image_path = '[jpg_png_or_gif_file_on_local_disk]'

  from google.cloud import automl_v1beta1 as automl

  automl_client = automl.AutoMlClient()

  # Get the full path of the model.
  model_full_id = automl_client.model_path(project_id, compute_region, model_id)

  prediction_client = automl.PredictionServiceClient()
  with open(local_image_path, 'rb') as f_in:
    image_bytes = f_in.read()
  payload = {'image': {'image_bytes': image_bytes}}
  result = prediction_client.predict(model_full_id, payload)
  print('Result of online predict: ', result)

  # [END automl_vision_iod_predict]


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  subparsers = parser.add_subparsers(dest='command')
  predict_parser = subparsers.add_parser('predict', help=predict.__doc__)
  predict_parser.add_argument('model_id')
  predict_parser.add_argument('input_uri')

  args = parser.parse_args()

  # Setup.
  project_id = os.environ['PROJECT_ID']
  compute_region = 'us-central1'

  if args.command == 'predict':
    predict(project_id, compute_region, args.model_id, args.input_uri)
