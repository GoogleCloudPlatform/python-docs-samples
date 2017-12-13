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

"""This application demonstrates face detection, label detection,
explicit content, and shot change detection using the Google Cloud API.

Usage Examples:

    python beta_snippets.py faces gs://demomaker/google_gmail.mp4
    python beta_snippets.py faces gs://sandboxdata/video_face/google_gmail_short.mp4
"""

import argparse
import io

from google.cloud import videointelligence_v1beta2 as videointelligence


def analyze_faces(path):
    """ Detects faces given a GCS path. """
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.FACE_DETECTION]

    config = videointelligence.types.FaceConfig(
        include_bounding_boxes=True)
    context = videointelligence.types.VideoContext(
        face_detection_config=config)

    operation = video_client.annotate_video(
        path, features=features, video_context=context)
    print('\nProcessing video for face annotations:')

    result = operation.result(timeout=600)
    print('\nFinished processing.')

    # first result is retrieved because a single video was processed
    faces = result.annotation_results[0].face_annotations
    for face_id, face in enumerate(faces):
        print('Face {}'.format(face_id))
        print('Thumbnail size: {}'.format(len(face.thumbnail)))

        for segment_id, segment in enumerate(face.segments):
            start_time = (segment.segment.start_time_offset.seconds +
                          segment.segment.start_time_offset.nanos / 1e9)
            end_time = (segment.segment.end_time_offset.seconds +
                        segment.segment.end_time_offset.nanos / 1e9)
            positions = '{}s to {}s'.format(start_time, end_time)
            print('\tSegment {}: {}'.format(segment_id, positions))

        # There are typically many frames for each face,
        # here we print information on only the first frame.
        frame = face.frames[0]
        time_offset = (frame.time_offset.seconds +
                       frame.time_offset.nanos / 1e9)
        box = frame.normalized_bounding_boxes[0]
        print('First frame time offset: {}s'.format(time_offset))
        print('First frame normalized bounding box:')
        print('\tleft: {}'.format(box.left))
        print('\ttop: {}'.format(box.top))
        print('\tright: {}'.format(box.right))
        print('\tbottom: {}'.format(box.bottom))
        print('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')
    analyze_faces_parser = subparsers.add_parser(
        'faces', help=analyze_faces.__doc__)
    analyze_faces_parser.add_argument('path')

    args = parser.parse_args()

    if args.command == 'faces':
        analyze_faces(args.path)
