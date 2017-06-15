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

"""This application demonstrates how to perform basic operations with the
Google Cloud Video Intelligence API.

For more information, check out the documentation at
https://cloud.google.com/videointelligence/docs.

Usage Example:

    python labels.py gs://cloud-ml-sandbox/video/chicago.mp4

"""

# [START full_tutorial]
# [START imports]
import argparse
import sys
import time

from google.cloud.gapic.videointelligence.v1beta1 import enums
from google.cloud.gapic.videointelligence.v1beta1 import (
    video_intelligence_service_client)
# [END imports]


def analyze_labels(path):
    """ Detects labels given a GCS path. """
    # [START construct_request]
    video_client = (video_intelligence_service_client.
                    VideoIntelligenceServiceClient())
    features = [enums.Feature.LABEL_DETECTION]
    operation = video_client.annotate_video(path, features)
    # [END construct_request]
    print('\nProcessing video for label annotations:')

    # [START check_operation]
    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(20)

    print('\nFinished processing.')
    # [END check_operation]

    # [START parse_response]
    results = operation.result().annotation_results[0]

    for label in results.label_annotations:
        print('Label description: {}'.format(label.description))
        print('Locations:')

        for l, location in enumerate(label.locations):
            print('\t{}: {} to {}'.format(
                l,
                location.segment.start_time_offset,
                location.segment.end_time_offset))
    # [END parse_response]


if __name__ == '__main__':
    # [START running_app]
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('path', help='GCS file path for label detection.')
    args = parser.parse_args()

    analyze_labels(args.path)
    # [END running_app]
# [END full_tutorial]
