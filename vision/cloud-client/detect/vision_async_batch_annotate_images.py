# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# DO NOT EDIT! This is a generated sample ("LongRunningPromise",  "vision_async_batch_annotate_images")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-vision

# sample-metadata
#   title: Async Batch Image Annotation
#   description: Perform async batch image annotation
#   usage: python3 samples/v1/vision_async_batch_annotate_images.py [--input_image_uri "gs://cloud-samples-data/vision/label/wakeupcat.jpg"] [--output_uri "gs://your-bucket/prefix/"]
import sys

# [START vision_async_batch_annotate_images]

from google.cloud import vision_v1
from google.cloud.vision_v1 import enums
import six

def sample_async_batch_annotate_images(input_image_uri, output_uri):
  """Perform async batch image annotation"""
  # [START vision_async_batch_annotate_images_core]

  client = vision_v1.ImageAnnotatorClient()

  # input_image_uri = 'gs://cloud-samples-data/vision/label/wakeupcat.jpg'
  # output_uri = 'gs://your-bucket/prefix/'

  if isinstance(input_image_uri, six.binary_type):
    input_image_uri = input_image_uri.decode('utf-8')
  if isinstance(output_uri, six.binary_type):
    output_uri = output_uri.decode('utf-8')
  source = {'image_uri': input_image_uri}
  image = {'source': source}
  type_ = enums.Feature.Type.LABEL_DETECTION
  features_element = {'type': type_}
  type_2 = enums.Feature.Type.IMAGE_PROPERTIES
  features_element_2 = {'type': type_2}
  features = [features_element, features_element_2]
  requests_element = {'image': image, 'features': features}
  requests = [requests_element]
  gcs_destination = {'uri': output_uri}

  # The max number of responses to output in each JSON file
  batch_size = 2
  output_config = {'gcs_destination': gcs_destination, 'batch_size': batch_size}

  operation = client.async_batch_annotate_images(requests, output_config)

  print('Waiting for operation to complete...')
  response = operation.result()

  # The output is written to GCS with the provided output_uri as prefix
  gcs_output_uri = response.output_config.gcs_destination.uri
  print('Output written to GCS with prefix: {}'.format(gcs_output_uri))

  # [END vision_async_batch_annotate_images_core]
# [END vision_async_batch_annotate_images]

def main():
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('--input_image_uri', type=str, default='gs://cloud-samples-data/vision/label/wakeupcat.jpg')
  parser.add_argument('--output_uri', type=str, default='gs://your-bucket/prefix/')
  args = parser.parse_args()

  sample_async_batch_annotate_images(args.input_image_uri, args.output_uri)

if __name__ == '__main__':
  main()