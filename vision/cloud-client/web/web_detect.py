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
from google.cloud.vision import types
# [END imports]


def annotate(path):
    """Returns web annotations given the path to an image."""
    # [START get_annotations]
    client = vision.ImageAnnotatorClient()

    if path.startswith('http') or path.startswith('gs:'):
        image = types.Image()
        image.source.image_uri = path

    else:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

    response = client.web_detection(image=image)
    web_detection = response.web_detection
    # [END get_annotations]

    return web_detection


def report(annotations):
    """Prints detected features in the provided web annotations."""
    # [START print_annotations]
    if annotations.best_guess_labels:
        for label in annotations.best_guess_labels:
            print('\nBest guess label: {}'.format(label.label))

    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images found:'.format(
            len(annotations.pages_with_matching_images)))

        for page in annotations.pages_with_matching_images:
            #print('\tTitle : {}'.format(page.page_title))
            print('\n\tPage url   : {}'.format(page.url))

            if page.full_matching_images:
                print('\t{} Full Matches found: '.format(
                       len(page.full_matching_images)))

                for image in page.full_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))

            if page.partial_matching_images:
                print('\t{} Partial Matches found: '.format(
                       len(page.partial_matching_images)))

                for image in page.partial_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))

    if annotations.web_entities:
        print('\n{} Web entities found: '.format(
            len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('\n\tScore      : {}'.format(entity.score))
            print('\tDescription: {}'.format(entity.description))

    if annotations.visually_similar_images:
        print('\n{} visually similar images found:\n'.format(
            len(annotations.visually_similar_images)))

        for image in annotations.visually_similar_images:
            print('\tImage url    : {}'.format(image.url))
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
