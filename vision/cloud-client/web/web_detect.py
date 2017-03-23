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

Example usage:
  python web_detect.py https://goo.gl/X4qcB6
  python web_detect.py ../detect/resources/landmark.jpg
  python web_detect.py gs://your-bucket/image.png
"""
# [START full_tutorial]
# [START imports]
import argparse
import io

from google.cloud import vision
# [END imports]


def annotate(path):
    """Returns web annotations given the path to an image."""
    # [START get_annotations]
    image = None
    vision_client = vision.Client()

    if path.startswith('http') or path.startswith('gs:'):
        image = vision_client.image(source_uri=path)

    else:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision_client.image(content=content)

    return image.detect_web()
    # [END get_annotations]


def report(annotations):
    """Prints detected features in the provided web annotations."""
    # [START print_annotations]
    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved')

        for page in annotations.pages_with_matching_images:
            print('Score : {}'.format(page.score))
            print('Url   : {}'.format(page.url))

    if annotations.full_matching_images:
        print ('\n{} Full Matches found: '.format(
               len(annotations.full_matching_images)))

        for image in annotations.full_matching_images:
            print('Score:  {}'.format(image.score))
            print('Url  : {}'.format(image.url))

    if annotations.partial_matching_images:
        print ('\n{} Partial Matches found: '.format(
               len(annotations.partial_matching_images)))

        for image in annotations.partial_matching_images:
            print('Score: {}'.format(image.score))
            print('Url  : {}'.format(image.url))

    if annotations.web_entities:
        print ('\n{} Web entities found: '.format(
            len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))
    # [END print_annotations]


if __name__ == '__main__':
    # [START run_web]
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    path_help = str('The image to detect, can be web URI, '
                    'Google Cloud Storage, or path to local file.')
    parser.add_argument('image_url', help=path_help)
    args = parser.parse_args()

    report(annotate(args.image_url))
    # [END run_web]
# [END full_tutorial]
