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

"""This application demonstrates how to identify all different shots
in a video using the Google Cloud Video Intelligence API.

For more information, check out the documentation at
https://cloud.google.com/videointelligence/docs.

Example Usage:

    python shotchange.py gs://demomaker/gbikes_dinosaur.mp4

"""

# [START full_tutorial]
# [START imports]
import argparse
import sys
import time

from google.cloud import videointelligence_v1beta2
from google.cloud.videointelligence_v1beta2 import enums
# [END imports]


def analyze_shots(path):
    """ Detects camera shot changes. """
    # [START construct_request]
    video_client = videointelligence_v1beta2.VideoIntelligenceServiceClient()
    features = [enums.Feature.SHOT_CHANGE_DETECTION]
    operation = video_client.annotate_video(path, features)
    # [END construct_request]
    print('\nProcessing video for shot change annotations:')

    # [START check_operation]
    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(20)

    print('\nFinished processing.')
    # [END check_operation]

    # [START parse_response]
    shots = operation.result().annotation_results[0].shot_annotations

    for i, shot in enumerate(shots):
        start_time = (shot.start_time_offset.seconds +
                      shot.start_time_offset.nanos / 1e9)
        end_time = (shot.end_time_offset.seconds +
                    shot.end_time_offset.nanos / 1e9)
        print('\tShot {}: {} to {}'.format(i, start_time, end_time))
    # [END parse_response]


if __name__ == '__main__':
    # [START running_app]
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('path', help='GCS path for shot change detection.')
    args = parser.parse_args()

    analyze_shots(args.path)
    # [END running_app]
# [END full_tutorial]
