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

Example Usage:

    python shotchange.py gs://demomaker/gbikes_dinosaur.mp4

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


def analyze_shots(path):
    """ Detects camera shot changes. """
    # [START construct_request]
    video_client = (video_intelligence_service_client.
                    VideoIntelligenceServiceClient())
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
    shots = operation.result().annotation_results[0]

    for note, shot in enumerate(shots.shot_annotations):
        print('Scene {}: {} to {}'.format(
            note,
            shot.start_time_offset,
            shot.end_time_offset))
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
