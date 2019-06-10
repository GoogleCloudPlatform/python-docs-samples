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

# DO NOT EDIT! This is a generated sample ("Request",  "vision_batch_annotate_files_gcs")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-vision

# sample-metadata
#   title:
#   description: Perform batch file annotation
#   usage: python3 samples/v1/vision_batch_annotate_files_gcs.py [--storage_uri "gs://cloud-samples-data/vision/document_understanding/kafka.pdf"]
import sys

# [START vision_batch_annotate_files_gcs]

from google.cloud import vision_v1
from google.cloud.vision_v1 import enums
import six

def sample_batch_annotate_files(storage_uri):
  """
    Perform batch file annotation

    Args:
      storage_uri Cloud Storage URI to source image in the format gs://[bucket]/
      [file]
    """
  # [START vision_batch_annotate_files_gcs_core]

  client = vision_v1.ImageAnnotatorClient()

  # storage_uri = 'gs://cloud-samples-data/vision/document_understanding/kafka.pdf'

  if isinstance(storage_uri, six.binary_type):
    storage_uri = storage_uri.decode('utf-8')
  gcs_source = {'uri': storage_uri}
  input_config = {'gcs_source': gcs_source}
  type_ = enums.Feature.Type.DOCUMENT_TEXT_DETECTION
  features_element = {'type': type_}
  features = [features_element]

  # The service can process up to 5 pages per document file.
  # Here we specify the first, second, and last page of the document to be
  # processed.
  pages_element = 1
  pages_element_2 = 2
  pages_element_3 = -1
  pages = [pages_element, pages_element_2, pages_element_3]
  requests_element = {'input_config': input_config, 'features': features, 'pages': pages}
  requests = [requests_element]

  response = client.batch_annotate_files(requests)
  for image_response in response.responses[0].responses:
    print('Full text: {}'.format(image_response.full_text_annotation.text))
    for page in image_response.full_text_annotation.pages:
      for block in page.blocks:
        print('\nBlock confidence: {}'.format(block.confidence))
        for par in block.paragraphs:
          print('\tParagraph confidence: {}'.format(par.confidence))
          for word in par.words:
            print('\t\tWord confidence: {}'.format(word.confidence))
            for symbol in word.symbols:
              print('\t\t\tSymbol: {}, (confidence: {})'.format(symbol.text, symbol.confidence))

  # [END vision_batch_annotate_files_gcs_core]
# [END vision_batch_annotate_files_gcs]

def main():
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('--storage_uri', type=str, default='gs://cloud-samples-data/vision/document_understanding/kafka.pdf')
  args = parser.parse_args()

  sample_batch_annotate_files(args.storage_uri)

if __name__ == '__main__':
  main()