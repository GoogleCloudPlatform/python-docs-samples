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

"""This application demonstrates how to detect labels from a video
based on the image content with the Google Cloud Video Intelligence
API.

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

from google.cloud import videointelligence_v1beta2
from google.cloud.videointelligence_v1beta2 import enums
# [END imports]


def analyze_labels(path):
    """ Detects labels given a GCS path. """
    # [START construct_request]
    video_client = videointelligence_v1beta2.VideoIntelligenceServiceClient()
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

    for i, segment_label in enumerate(results.segment_label_annotations):
        print('Video label description: {}'.format(
            segment_label.entity.description))
        for category_entity in segment_label.category_entities:
            print('\tLabel category description: {}'.format(
                category_entity.description))

        for i, segment in enumerate(segment_label.segments):
            start_time = (segment.segment.start_time_offset.seconds +
                          segment.segment.start_time_offset.nanos / 1e9)
            end_time = (segment.segment.end_time_offset.seconds +
                        segment.segment.end_time_offset.nanos / 1e9)
            positions = '{}s to {}s'.format(start_time, end_time)
            confidence = segment.confidence
            print('\tSegment {}: {}'.format(i, positions))
            print('\tConfidence: {}'.format(confidence))
        print('\n')
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
