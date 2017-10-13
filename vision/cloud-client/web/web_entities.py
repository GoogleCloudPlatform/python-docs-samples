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

This sample prints only web_entities allowing the user to specify
whether to include geo_results, which are based on GPS information
included in the image.  Use the "--include-geo-results" flag to turn on
the geo entities feature.

Example usage:
  python web_entities.py https://goo.gl/X4qcB6 --include-geo-results
  python web_entities.py ../detect/resources/city.jpg --include-geo-results
  python web_entities.py gs://your-bucket/image.png --include-geo-results
"""
# [START imports]
import argparse
import io

from google.cloud import vision
from google.cloud.vision import types
# [END imports]


# [START def_annotate_web_entities]
def annotate_web_entities(path, include_geo_results=False):
    """Returns web annotations given the path to an image."""
    client = vision.ImageAnnotatorClient()

    if path.startswith('http') or path.startswith('gs:'):
        image = types.Image()
        image.source.image_uri = path

    else:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

    web_detection_params = types.WebDetectionParams(
        include_geo_results=include_geo_results)
    image_context = types.ImageContext(
        web_detection_params=web_detection_params)

    response = client.web_detection(image=image, image_context=image_context)

    web_detection = response.web_detection
    web_entities = web_detection.web_entities

    for entity in web_entities:
        print(u'\nDescription: {}'.format(entity.description))
        print('Score: {}'.format(entity.score))
# [END def_annotate_web_entities]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    path_help = str('The image to detect, can be web URI, '
                    'Google Cloud Storage, or path to local file.')
    parser.add_argument('image_url', help=path_help)
    parser.add_argument(
        '--include-geo-results', action='store_true', default=False,
        help='Use GPS signal in image to find geo entities.')
    args = parser.parse_args()

    annotate_web_entities(args.image_url, args.include_geo_results)
