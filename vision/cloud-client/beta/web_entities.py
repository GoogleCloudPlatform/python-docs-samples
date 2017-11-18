#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
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

"""Demonstrates web detection using the Google Cloud Vision API.

This sample prints web_entities detected with `include geo_results`
turned off.

Example usage:
  python web_entities.py \
  --image-uri https://goo.gl/X4qcB6
  python web_entities.py \
  --image-uri gs://your-bucket/image.png
  python web_entities.py \
  --image-file-path ../detect/resources/city.jpg
"""
# [START imports]
import argparse
import io

from google.cloud import vision_v1p1beta1 as vision
# [END imports]


# [START vision_web_entities_uri]
def web_entities_uri(image_uri):
    client = vision.ImageAnnotatorClient()

    image = vision.types.Image()
    image.source.image_uri = image_uri

    response = client.web_detection(image=image)

    for entity in response.web_detection.web_entities:
        print(u'\nDescription: {}'.format(entity.description))
        print('Score: {}'.format(entity.score))
# [END vision_web_entities_uri]


# [START vision_web_entities_file]
def web_entities_file(image_file_path):
    client = vision.ImageAnnotatorClient()

    with io.open(image_file_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.web_detection(image=image)

    for entity in response.web_detection.web_entities:
        print(u'\nDescription: {}'.format(entity.description))
        print('Score: {}'.format(entity.score))
# [END vision_web_entities_file]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        '--image-uri',
        help='Web URI or Google Cloud Storage URI.')
    source.add_argument(
        '--image-file-path',
        help='Path to local image file.')

    args = parser.parse_args()

    if args.image_uri:
        web_entities_uri(args.image_uri)
    else:
        web_entities_file(args.image_file_path)
