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
"""

import argparse
import sys
import time

from google.cloud.gapic.videointelligence.v1beta1 import enums
from google.cloud.gapic.videointelligence.v1beta1 import (
    video_intelligence_service_client)


def analyze_faces(path):
    """ Detects faces given a GCS path. """
    video_client = (video_intelligence_service_client.
                    VideoIntelligenceServiceClient())
    features = [enums.Feature.FACE_DETECTION]
    operation = video_client.annotate_video(path, features)
    print('\nProcessing video for label annotations:')

    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)

    print('\nFinished processing.')

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


def analyze_labels(path):
    """ Detects labels given a GCS path. """
    video_client = (video_intelligence_service_client.
                    VideoIntelligenceServiceClient())
    features = [enums.Feature.LABEL_DETECTION]
    operation = video_client.annotate_video(path, features)
    print('\nProcessing video for label annotations:')

    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)

    print('\nFinished processing.')

    # first result is retrieved because a single video was processed
    results = operation.result().annotation_results[0]

    for i, label in enumerate(results.label_annotations):
        print('Label description: {}'.format(label.description))
        print('Locations:')

        for l, location in enumerate(label.locations):
            print('\t{}: {} to {}'.format(
                l,
                location.segment.start_time_offset,
                location.segment.end_time_offset))


def analyze_shots(path):
    """ Detects camera shot changes. """
    video_client = (video_intelligence_service_client.
                    VideoIntelligenceServiceClient())
    features = [enums.Feature.SHOT_CHANGE_DETECTION]
    operation = video_client.annotate_video(path, features)
    print('\nProcessing video for shot change annotations:')

    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)

    print('\nFinished processing.')

    # first result is retrieved because a single video was processed
    shots = operation.result().annotation_results[0]

    for note, shot in enumerate(shots.shot_annotations):
        print('Scene {}: {} to {}'.format(
            note,
            shot.start_time_offset,
            shot.end_time_offset))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')
    analyze_faces_parser = subparsers.add_parser(
        'faces', help=analyze_faces.__doc__)
    analyze_faces_parser.add_argument('path')
    analyze_labels_parser = subparsers.add_parser(
        'labels', help=analyze_labels.__doc__)
    analyze_labels_parser.add_argument('path')
    analyze_shots_parser = subparsers.add_parser(
        'shots', help=analyze_shots.__doc__)
    analyze_shots_parser.add_argument('path')

    args = parser.parse_args()

    if args.command == 'faces':
        analyze_faces(args.path)
    if args.command == 'labels':
        analyze_labels(args.path)
    if args.command == 'shots':
        analyze_shots(args.path)
