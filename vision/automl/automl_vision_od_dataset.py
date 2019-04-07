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


def encode_image_example(image):
  """Demonstrate how to base64 an image (or any file)."""
  # Import the base64 encoding library.
  import base64

  # Pass the image data to an encoding function.
  def encode_image(image):
    image_content = image.read()
    return base64.b64encode(image_content)

  return encode_image(image)


def create_dataset(project_id, compute_region, dataset_name):
  """Creates a dataset."""
  # [START automl_vision_iod_create_dataset]
  ## To do: Uncomment and set the following variables
  # project_id = '[PROJECT_ID]'
  # compute_region = '[COMPUTE_REGION]'
  # dataset_name = '[DATASET_NAME]'

  from google.cloud import automl_v1beta1 as automl

  client = automl.AutoMlClient()

  # A resource that represents Google Cloud Platform location.
  project_location = client.location_path(project_id, compute_region)

  # Set dataset name and metadata of the dataset.
  my_dataset = {
      'display_name': dataset_name,
      'image_object_detection_dataset_metadata': {},
  }

  # Create a dataset with the dataset metadata in the region.
  dataset = client.create_dataset(project_location, my_dataset)

  # Display the dataset information.
  print('Dataset name: {}'.format(dataset.name))
  print('Dataset id: {}'.format(dataset.name.split('/')[-1]))
  print('Dataset display name: {}'.format(dataset.display_name))
  print('Dataset example count: {}'.format(dataset.example_count))
  print('Dataset create time:')
  print('\tseconds: {}'.format(dataset.create_time.seconds))
  print('\tnanos: {}'.format(dataset.create_time.nanos))
  dataset_spec = {}
  my_dataset = {
      'display_name': dataset_name,
      'image_object_detection_dataset_metadata': dataset_spec
  }
  response = client.create_dataset(project_location, my_dataset)
  print('\nDataset creation: {}'.format(response))
  dataset_full_id = response.name
  print('Dataset full id: {}'.format(dataset_full_id))

  # [END automl_vision_iod_create_dataset]


def get_dataset(project_id, compute_region, dataset_id):
  """Describes a dataset."""
  # [START automl_vision_iod_get_dataset]
  ## To do: Uncomment and set the following variables
  # project_id = '[PROJECT_ID]'
  # compute_region = '[COMPUTE_REGION]'
  # dataset_id = '[DATASET_ID]'

  from google.cloud import automl_v1beta1 as automl

  client = automl.AutoMlClient()

  # A resource that represents Google Cloud Platform location.
  project_location = client.location_path(project_id, compute_region)

  # Get the full path of the dataset.
  dataset_full_id = client.dataset_path(project_id, compute_region, dataset_id)

  # Get the dataset
  response = client.get_dataset(dataset_full_id)
  print('\nDataset description: {}'.format(response))

  # [END automl_vision_iod_get_dataset]


def list_datasets(project_id, compute_region, filter_):
  """Lists all datasets."""
  # [START automl_vision_iod_lists_dataset]
  ## To do: Uncomment and set the following variables
  # project_id = '[PROJECT_ID]'
  # compute_region = '[COMPUTE_REGION]'
  # filter_ = ''

  from google.cloud import automl_v1beta1 as automl

  client = automl.AutoMlClient()

  # A resource that represents Google Cloud Platform location.
  project_location = client.location_path(project_id, compute_region)

  # List all the datasets available in the region by applying filter.
  response = client.list_datasets(project_location, filter_=filter_)

  print('List of datasets:')
  for dataset in response:
    # Display the dataset information.
    print('Dataset name: {}'.format(dataset.name))
    print('Dataset id: {}'.format(dataset.name.split('/')[-1]))
    print('Dataset display name: {}'.format(dataset.display_name))
    print('Dataset example count: {}'.format(dataset.example_count))
    print('Dataset create time:')
    print('\tseconds: {}'.format(dataset.create_time.seconds))
    print('\tnanos: {}'.format(dataset.create_time.nanos))

  # [END automl_vision_iod_lists_dataset]


def import_data(project_id, compute_region, dataset_id, paths):
  """Imports images and bounding boxes."""
  # [START automl_vision_iod_import_data]
  ## To do: Uncomment and set the following variables
  # project_id = '[PROJECT_ID]'
  # compute_region = '[COMPUTE_REGION]'
  # dataset_id = '[DATASET_ID]'
  # paths = '[Storage path. For example: gs://path/to/file.csv]'

  from google.cloud import automl_v1beta1 as automl

  client = automl.AutoMlClient()

  # Get the full path of the dataset.
  dataset_full_id = client.dataset_path(project_id, compute_region, dataset_id)

  # Get the multiple Google Cloud Storage URIs.
  input_config = {'gcs_source': {'input_uris': paths}}

  # Import data from the input URI.
  response = client.import_data(dataset_full_id, input_config)

  print('Processing import...')
  # synchronous check of operation status.
  print('Data imported. {}'.format(response.result()))

  # [END automl_vision_iod_import_data]


def delete_dataset(project_id, compute_region, dataset_id):
  """Deletes a dataset."""
  # [START automl_vision_iod_delete_dataset]
  ## To do: Uncomment and set the following variables
  # project_id = '[PROJECT_ID]'
  # compute_region = '[COMPUTE_REGION]'
  # dataset_id = '[DATASET_ID]'

  from google.cloud import automl_v1beta1 as automl

  client = automl.AutoMlClient()

  # Get the full path of the dataset.
  dataset_full_id = client.dataset_path(project_id, compute_region, dataset_id)

  # Delete a dataset.
  response = client.delete_dataset(dataset_full_id)

  # synchronous check of operation status.
  print('Dataset deleted. {}'.format(response.result()))

  # [END automl_vision_iod_delete_dataset]


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  subparsers = parser.add_subparsers(dest='command')
  create_dataset_parser = subparsers.add_parser(
      'create_dataset', help=create_dataset.__doc__)
  create_dataset_parser.add_argument('dataset_name')
  get_dataset_parser = subparsers.add_parser(
      'get_dataset', help=get_dataset.__doc__)
  get_dataset_parser.add_argument('dataset_id')
  import_data_parser = subparsers.add_parser(
      'import_data', help=import_data.__doc__)
  import_data_parser.add_argument('path')
  import_data_parser.add_argument('dataset_id')
  list_datasets_parser = subparsers.add_parser(
      'list_datasets', help=list_datasets.__doc__)
  delete_dataset_parser = subparsers.add_parser(
      'delete_dataset', help=delete_dataset.__doc__)
  delete_dataset_parser.add_argument('dataset_id')

  args = parser.parse_args()

  # Setup.
  project_id = os.environ['PROJECT_ID']
  compute_region = 'us-central1'

  if args.command == 'create_dataset':
    create_dataset(project_id, compute_region, args.dataset_name)
  if args.command == 'get_dataset':
    get_dataset(project_id, compute_region, args.dataset_id)
  if args.command == 'delete_dataset':
    delete_dataset(project_id, compute_region, args.dataset_id)
  if args.command == 'list_datasets':
    list_datasets(project_id, compute_region, '')
  if args.command == 'import_data':
    import_data(project_id, compute_region, args.dataset_id, [args.path])
