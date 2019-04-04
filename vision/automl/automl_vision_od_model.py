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


def create_model(project_id, compute_region, dataset_id, model_name):
  """Starts model training."""
  # [START automl_vision_iod_create_model]
  ## To do: Uncomment and set the following variables
  # project_id = '[PROJECT_ID]'
  # compute_region = '[COMPUTE_REGION]'
  # dataset_id = '[DATASET_ID]' # From the previous step. N.B. id != display_name
  # model_name = '[MODEL_NAME]'

  from google.cloud import automl_v1beta1 as automl

  client = automl.AutoMlClient()

  # A resource that represents Google Cloud Platform location.
  project_location = client.location_path(project_id, compute_region)

  # Set model name and model metadata for the image dataset.
  my_model = {
      'display_name': model_name,
      'dataset_id': dataset_id,
      'image_object_detection_model_metadata': {}
  }

  # Create a model with the model metadata in the region.
  response = client.create_model(project_location, my_model)

  print('Training operation name: {}'.format(response.operation.name))
  print('Training started...')

  # [END automl_vision_iod_create_model]


def get_model(project_id, compute_region, model_id):
  """Describes a model."""
  # [START automl_vision_iod_get_model]
  ## To do: Uncomment and set the following variables
  # project_id = '[PROJECT_ID]'
  # compute_region = '[COMPUTE_REGION]'
  # model_id = '[MODEL_ID]' # From the previous create step. N.B. id != display_name

  from google.cloud import automl_v1beta1 as automl
  from google.cloud.automl_v1beta1 import enums

  client = automl.AutoMlClient()

  # Get the full path of the model.
  model_full_id = client.model_path(project_id, compute_region, model_id)

  # Get complete detail of the model.
  model = client.get_model(model_full_id)

  # Retrieve deployment state.
  if model.deployment_state == enums.Model.DeploymentState.DEPLOYED:
    deployment_state = 'deployed'
  else:
    deployment_state = 'undeployed'

  # Display the model information.
  print('Model name: {}'.format(model.name))
  print('Model id: {}'.format(model.name.split('/')[-1]))
  print('Model display name: {}'.format(model.display_name))
  print('Model create time:')
  print('\tseconds: {}'.format(model.create_time.seconds))
  print('\tnanos: {}'.format(model.create_time.nanos))
  print('Model deployment state: {}'.format(deployment_state))

  # [END automl_vision_iod_get_model]


def list_models(project_id, compute_region, filter_):
  """Lists all models."""
  # [START automl_vision_iod_list_models]
  ## To do: Uncomment and set the following variables
  # project_id = '[PROJECT_ID]'
  # compute_region = '[COMPUTE_REGION]'
  # filter_ = ''

  from google.cloud import automl_v1beta1 as automl
  from google.cloud.automl_v1beta1 import enums

  client = automl.AutoMlClient()

  # A resource that represents Google Cloud Platform location.
  project_location = client.location_path(project_id, compute_region)

  # List all the models available in the region by applying filter.
  response = client.list_models(project_location, filter_)

  print('List of models:')
  for model in response:
    # Retrieve deployment state.
    if model.deployment_state == enums.Model.DeploymentState.DEPLOYED:
      deployment_state = 'deployed'
    else:
      deployment_state = 'undeployed'

    # Display the model information.
    print('Model name: {}'.format(model.name))
    print('Model id: {}'.format(model.name.split('/')[-1]))
    print('Model display name: {}'.format(model.display_name))
    print('Model create time:')
    print('\tseconds: {}'.format(model.create_time.seconds))
    print('\tnanos: {}'.format(model.create_time.nanos))
    print('Model deployment state: {}'.format(deployment_state))

  # [END automl_vision_iod_list_models]


def delete_model(project_id, compute_region, model_id):
  """Deletes a model."""
  # [START automl_vision_iod_delete_model]
  ## To do: Uncomment and set the following variables
  # project_id = '[PROJECT_ID]'
  # compute_region = '[COMPUTE_REGION]'
  # model_id = '[MODEL_ID]'

  from google.cloud import automl_v1beta1 as automl

  client = automl.AutoMlClient()

  # Get the full path of the model.
  model_full_id = client.model_path(project_id, compute_region, model_id)

  # Delete a model.
  response = client.delete_model(model_full_id)

  # synchronous check of operation status.
  print('Model deleted. {}'.format(response.result()))

  # [END automl_vision_iod_delete_model]


def list_model_evaluations(project_id, compute_region, model_id, filter_):
  """Lists model evaluations."""
  # [START automl_vision_iod_list_model_evaluations]
  ## To do: Uncomment and set the following variables
  # project_id = '[PROJECT_ID]'
  # compute_region = '[COMPUTE_REGION]'
  # model_id = '[MODEL_ID]'
  # filter_ = ''

  from google.cloud import automl_v1beta1 as automl

  client = automl.AutoMlClient()

  # Get the full path of the model.
  model_full_id = client.model_path(project_id, compute_region, model_id)

  # List all the model evaluations in the model by applying filter.
  response = client.list_model_evaluations(model_full_id, filter_)

  print('List of model evaluations:')
  for element in response:
    print(element)

  # [END automl_vision_iod_list_model_evaluations]

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  subparsers = parser.add_subparsers(dest='command')
  create_model_parser = subparsers.add_parser(
      'create_model', help=create_model.__doc__)
  create_model_parser.add_argument('dataset_id')
  create_model_parser.add_argument('model_name')
  list_models_parser = subparsers.add_parser(
      'list_models', help=list_models.__doc__)
  get_model_parser = subparsers.add_parser('get_model', help=get_model.__doc__)
  get_model_parser.add_argument('model_id')
  delete_model_parser = subparsers.add_parser(
      'delete_model', help=delete_model.__doc__)
  delete_model_parser.add_argument('model_id')
  list_model_evaluations_parser = subparsers.add_parser(
      'list_model_evaluations', help=list_model_evaluations.__doc__)
  list_model_evaluations_parser.add_argument('model_id')

  args = parser.parse_args()

  # Setup.
  project_id = os.environ['PROJECT_ID']
  compute_region = 'us-central1'

  if args.command == 'create_model':
    create_model(project_id, compute_region, args.dataset_id, args.model_name)
  if args.command == 'delete_model':
    delete_model(project_id, compute_region, args.model_id)
  if args.command == 'list_models':
    list_models(project_id, compute_region, '')
  if args.command == 'get_model':
    get_model(project_id, compute_region, args.model_id)
  if args.command == 'list_model_evaluations':
    list_model_evaluations(project_id, compute_region, args.model_id, '')
