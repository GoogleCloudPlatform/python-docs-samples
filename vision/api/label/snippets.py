#!/usr/bin/env python
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import base64
import json

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials

DISCOVERY_URL = (
    'https://vision.googleapis.com/$discovery/rest?'
    'labels=TRUSTED_TESTER&version=v1'
)


def get_service():
    """Get vision service using discovery."""
    credentials = GoogleCredentials.get_application_default()
    scoped_credentials = credentials.create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    scoped_credentials.authorize(http)
    return discovery.build(
        'vision', 'v1',
        http=http,
        discoveryServiceUrl=DISCOVERY_URL
    )


def crop_hint(photo_file):
    """Run a crop hint request on the image."""

    service = get_service()

    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())

    service_request = service.images().annotate(body={
        'requests': [{
            'image': {
                'content': image_content.decode('UTF-8')
            },
            'features': [{
                'type': 'CROP_HINTS'
            }]
        }]
    })

    response = service_request.execute()
    print(json.dumps(response, indent=2))


def web_annotation(photo_file):
    """Run a web annotation request on the image."""

    service = get_service()

    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())

    service_request = service.images().annotate(body={
        'requests': [{
            'image': {
                'content': image_content.decode('UTF-8')
            },
            'features': [{
                'type': 'WEB_ANNOTATION',
                'maxResults': 10
            }]
        }]
    })

    response = service_request.execute()
    print(json.dumps(response, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['crop_hint', 'web_annotation'])
    parser.add_argument('image_file', help='The image you\'d like to process.')
    args = parser.parse_args()

    if args.command == 'crop_hint':
        response = crop_hint(args.image_file)
    elif args.command == 'web_annotation':
        response = web_annotation(args.image_file)
