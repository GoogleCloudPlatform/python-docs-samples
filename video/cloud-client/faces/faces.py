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

"""This application demonstrates how to perform shot change detection with the
Google Cloud Video Intelligence API.

For more information, check out the documentation at
https://cloud.google.com/videointelligence/docs.

Usage Example:

    python faces.py gs://demomaker/google_gmail.mp4

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


def analyze_faces(path):
    # [START construct_request]
    """ Detects faces given a GCS path. """
    video_client = (video_intelligence_service_client.
                    VideoIntelligenceServiceClient())
    features = [enums.Feature.FACE_DETECTION]
    operation = video_client.annotate_video(path, features)
    # [END construct_request]
    print('\nProcessing video for face annotations:')

    # [START check_operation]
    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(20)

    print('\nFinished processing.')
    # [END check_operation]

    # [START parse_response]
    # first result is retrieved because a single video was processed
    face_annotations = (operation.result().annotation_results[0].
                        face_annotations)

    for face_id, face in enumerate(face_annotations):
        print('Thumbnail size: {}'.format(len(face.thumbnail)))

        for segment_id, segment in enumerate(face.segments):
            print('Track {}: {} to {}'.format(
                segment_id,
                segment.start_time_offset,
                segment.end_time_offset))
    # [END parse_response]


if __name__ == '__main__':
    # [START running_app]
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('path', help='GCS file path for face detection.')
    args = parser.parse_args()

    analyze_faces(args.path)
    # [END running_app]
# [END full_tutorial]
