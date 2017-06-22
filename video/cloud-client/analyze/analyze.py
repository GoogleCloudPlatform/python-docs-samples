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

"""This application demonstrates face detection, label detection, safe search,
and shot change detection using the Google Cloud API.

Usage Examples:

    python analyze.py faces gs://demomaker/google_gmail.mp4
    python analyze.py labels gs://cloud-ml-sandbox/video/chicago.mp4
    python analyze.py labels_file resources/cat.mp4
    python analyze.py shots gs://demomaker/gbikes_dinosaur.mp4
    python analyze.py safe_search gs://demomaker/gbikes_dinosaur.mp4

"""

import argparse
import base64
import io
import sys
import time

from google.cloud.gapic.videointelligence.v1beta1 import enums
from google.cloud.gapic.videointelligence.v1beta1 import (
    video_intelligence_service_client)


def analyze_safe_search(path):
    """ Detects safe search features the GCS path to a video. """
    video_client = (video_intelligence_service_client.
                    VideoIntelligenceServiceClient())
    features = [enums.Feature.SAFE_SEARCH_DETECTION]
    operation = video_client.annotate_video(path, features)
    print('\nProcessing video for safe search annotations:')

    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(15)

    print('\nFinished processing.')

    # first result is retrieved because a single video was processed
    safe_annotations = (operation.result().annotation_results[0].
                        safe_search_annotations)

    likely_string = ("Unknown", "Very unlikely", "Unlikely", "Possible",
                     "Likely", "Very likely")

    for note in safe_annotations:
        print('Time: {}s'.format(note.time_offset / 1000000.0))
        print('\tadult: {}'.format(likely_string[note.adult]))
        print('\tspoof: {}'.format(likely_string[note.spoof]))
        print('\tmedical: {}'.format(likely_string[note.medical]))
        print('\tracy: {}'.format(likely_string[note.racy]))
        print('\tviolent: {}\n'.format(likely_string[note.violent]))


def analyze_faces(path):
    """ Detects faces given a GCS path. """
    video_client = (video_intelligence_service_client.
                    VideoIntelligenceServiceClient())
    features = [enums.Feature.FACE_DETECTION]
    operation = video_client.annotate_video(path, features)
    print('\nProcessing video for face annotations:')

    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(15)

    print('\nFinished processing.')

    # first result is retrieved because a single video was processed
    face_annotations = (operation.result().annotation_results[0].
                        face_annotations)

    for face_id, face in enumerate(face_annotations):
        print('Thumbnail size: {}'.format(len(face.thumbnail)))

        for segment_id, segment in enumerate(face.segments):
            positions = 'Entire video'
            if (segment.start_time_offset != -1 or
                    segment.end_time_offset != -1):
                positions = '{}s to {}s'.format(
                    segment.start_time_offset / 1000000.0,
                    segment.end_time_offset / 1000000.0)

            print('\tTrack {}: {}'.format(segment_id, positions))

        print('\n')


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
        time.sleep(15)

    print('\nFinished processing.')

    # first result is retrieved because a single video was processed
    results = operation.result().annotation_results[0]

    for i, label in enumerate(results.label_annotations):
        print('Label description: {}'.format(label.description))
        print('Locations:')

        for l, location in enumerate(label.locations):
            positions = 'Entire video'
            if (location.segment.start_time_offset != -1 or
                    location.segment.end_time_offset != -1):
                positions = '{}s to {}s'.format(
                    location.segment.start_time_offset / 1000000.0,
                    location.segment.end_time_offset / 1000000.0)
            print('\t{}: {}'.format(l, positions))

        print('\n')


def analyze_labels_file(path):
    """ Detects labels given a file path. """
    video_client = (video_intelligence_service_client.
                    VideoIntelligenceServiceClient())
    features = [enums.Feature.LABEL_DETECTION]

    with io.open(path, "rb") as movie:
        content_base64 = base64.b64encode(movie.read())

    operation = video_client.annotate_video(
        '', features, input_content=content_base64)
    print('\nProcessing video for label annotations:')

    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(15)

    print('\nFinished processing.')

    # first result is retrieved because a single video was processed
    results = operation.result().annotation_results[0]

    for i, label in enumerate(results.label_annotations):
        print('Label description: {}'.format(label.description))
        print('Locations:')

        for l, location in enumerate(label.locations):
            positions = 'Entire video'
            if (location.segment.start_time_offset != -1 or
                    location.segment.end_time_offset != -1):
                positions = '{} to {}'.format(
                    location.segment.start_time_offset / 1000000.0,
                    location.segment.end_time_offset / 1000000.0)
            print('\t{}: {}'.format(l, positions))

        print('\n')


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
        time.sleep(15)

    print('\nFinished processing.')

    # first result is retrieved because a single video was processed
    shots = operation.result().annotation_results[0]

    for note, shot in enumerate(shots.shot_annotations):
        print('\tScene {}: {} to {}'.format(
            note,
            shot.start_time_offset / 1000000.0,
            shot.end_time_offset / 1000000.0))


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
    analyze_labels_file_parser = subparsers.add_parser(
        'labels_file', help=analyze_labels_file.__doc__)
    analyze_labels_file_parser.add_argument('path')
    analyze_safe_search_parser = subparsers.add_parser(
        'safe_search', help=analyze_safe_search.__doc__)
    analyze_safe_search_parser.add_argument('path')
    analyze_shots_parser = subparsers.add_parser(
        'shots', help=analyze_shots.__doc__)
    analyze_shots_parser.add_argument('path')

    args = parser.parse_args()

    if args.command == 'faces':
        analyze_faces(args.path)
    if args.command == 'labels':
        analyze_labels(args.path)
    if args.command == 'labels_file':
        analyze_labels_file(args.path)
    if args.command == 'shots':
        analyze_shots(args.path)
    if args.command == 'safe_search':
        analyze_safe_search(args.path)
