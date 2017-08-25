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
    python analyze.py explicit_content gs://demomaker/gbikes_dinosaur.mp4

"""

import argparse
import base64
import io
import sys
import time

from google.cloud import videointelligence_v1beta2
from google.cloud.videointelligence_v1beta2 import enums
from google.cloud.videointelligence_v1beta2 import types

def analyze_explicit_content(path):
    """ Detects explicit content from the GCS path to a video. """
    video_client = videointelligence_v1beta2.VideoIntelligenceServiceClient()
    features = [enums.Feature.EXPLICIT_CONTENT_DETECTION]

    operation = video_client.annotate_video(path, features)
    print('\nProcessing video for explicit content annotations:')

    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(15)

    print('\nFinished processing.')

    # first result is retrieved because a single video was processed
    explicit_annotation = (operation.result().annotation_results[0].
                        explicit_annotation)

    likely_string = ("Unknown", "Very unlikely", "Unlikely", "Possible",
                     "Likely", "Very likely")

    for frame in explicit_annotation.frames:
        frame_time = frame.time_offset.seconds + frame.time_offset.nanos / 1e9
        print('Time: {}s'.format(frame_time))
        print('\tpornography: {}'.format(likely_string[frame.pornography_likelihood]))


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
    video_client = videointelligence_v1beta2.VideoIntelligenceServiceClient()
    features = [enums.Feature.SHOT_CHANGE_DETECTION]
    operation = video_client.annotate_video(path, features)
    print('\nProcessing video for shot change annotations:')

    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(15)

    print('\nFinished processing.')

    # first result is retrieved because a single video was processed
    shots = operation.result().annotation_results[0].shot_annotations

    for i, shot in enumerate(shots):
        start_time = shot.start_time_offset.seconds + shot.end_time_offset.nanos / 1e9
        end_time = shot.end_time_offset.seconds + shot.end_time_offset.nanos / 1e9
        print('\tScene {}: {} to {}'.format(i, start_time, end_time))


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
    analyze_explicit_content_parser = subparsers.add_parser(
        'explicit_content', help=analyze_explicit_content.__doc__)
    analyze_explicit_content_parser.add_argument('path')
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
    if args.command == 'explicit_content':
        analyze_explicit_content(args.path)
