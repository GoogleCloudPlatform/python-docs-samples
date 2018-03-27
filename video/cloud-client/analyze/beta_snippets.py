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

"""This application demonstrates face detection, face emotions
and speech transcription using the Google Cloud API.

Usage Examples:
    python beta_snippets.py boxes \
    gs://python-docs-samples-tests/video/googlework_short.mp4

    python beta_snippets.py \
    emotions gs://python-docs-samples-tests/video/googlework_short.mp4

    python beta_snippets.py \
    transcription gs://python-docs-samples-tests/video/googlework_short.mp4
"""

import argparse

from google.cloud import videointelligence_v1p1beta1 as videointelligence


# [START video_face_bounding_boxes]
def face_bounding_boxes(gcs_uri):
    """ Detects faces' bounding boxes. """
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.FACE_DETECTION]

    config = videointelligence.types.FaceConfig(
        include_bounding_boxes=True)
    context = videointelligence.types.VideoContext(
        face_detection_config=config)

    operation = video_client.annotate_video(
        gcs_uri, features=features, video_context=context)
    print('\nProcessing video for face annotations:')

    result = operation.result(timeout=900)
    print('\nFinished processing.')

    # There is only one result because a single video was processed.
    faces = result.annotation_results[0].face_detection_annotations
    for i, face in enumerate(faces):
        print('Face {}'.format(i))

        # Each face_detection_annotation has only one segment.
        segment = face.segments[0]
        start_time = (segment.segment.start_time_offset.seconds +
                      segment.segment.start_time_offset.nanos / 1e9)
        end_time = (segment.segment.end_time_offset.seconds +
                    segment.segment.end_time_offset.nanos / 1e9)
        positions = '{}s to {}s'.format(start_time, end_time)
        print('\tSegment: {}\n'.format(positions))

        # Each detected face may appear in many frames of the video.
        # Here we process only the first frame.
        frame = face.frames[0]

        time_offset = (frame.time_offset.seconds +
                       frame.time_offset.nanos / 1e9)
        box = frame.attributes[0].normalized_bounding_box

        print('First frame time offset: {}s\n'.format(time_offset))

        print('First frame normalized bounding box:')
        print('\tleft  : {}'.format(box.left))
        print('\ttop   : {}'.format(box.top))
        print('\tright : {}'.format(box.right))
        print('\tbottom: {}'.format(box.bottom))
        print('\n')
# [END video_face_bounding_boxes]


# [START video_face_emotions]
def face_emotions(gcs_uri):
    """ Analyze faces' emotions over frames. """
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.FACE_DETECTION]

    config = videointelligence.types.FaceConfig(
        include_emotions=True)
    context = videointelligence.types.VideoContext(
        face_detection_config=config)

    operation = video_client.annotate_video(
        gcs_uri, features=features, video_context=context)
    print('\nProcessing video for face annotations:')

    result = operation.result(timeout=600)
    print('\nFinished processing.')

    # There is only one result because a single video was processed.
    faces = result.annotation_results[0].face_detection_annotations
    for i, face in enumerate(faces):
        for j, frame in enumerate(face.frames):
            time_offset = (frame.time_offset.seconds +
                           frame.time_offset.nanos / 1e9)
            emotions = frame.attributes[0].emotions

            print('Face {}, frame {}, time_offset {}\n'.format(
                i, j, time_offset))

            # from videointelligence.enums
            emotion_labels = (
                'EMOTION_UNSPECIFIED', 'AMUSEMENT', 'ANGER',
                'CONCENTRATION', 'CONTENTMENT', 'DESIRE',
                'DISAPPOINTMENT', 'DISGUST', 'ELATION',
                'EMBARRASSMENT', 'INTEREST', 'PRIDE', 'SADNESS',
                'SURPRISE')

            for emotion in emotions:
                emotion_index = emotion.emotion
                emotion_label = emotion_labels[emotion_index]
                emotion_score = emotion.score

                print('emotion: {} (confidence score: {})'.format(
                    emotion_label, emotion_score))

            print('\n')

        print('\n')
# [END video_face_emotions]


# [START video_speech_transcription]
def speech_transcription(input_uri):
    """Transcribe speech from a video stored on GCS."""
    video_client = videointelligence.VideoIntelligenceServiceClient()

    features = [videointelligence.enums.Feature.SPEECH_TRANSCRIPTION]

    config = videointelligence.types.SpeechTranscriptionConfig(
        language_code='en-US')
    video_context = videointelligence.types.VideoContext(
        speech_transcription_config=config)

    operation = video_client.annotate_video(
        input_uri, features=features,
        video_context=video_context)

    print('\nProcessing video for speech transcription.')

    result = operation.result(timeout=180)

    # There is only one annotation_result since only
    # one video is processed.
    annotation_results = result.annotation_results[0]
    speech_transcription = annotation_results.speech_transcriptions[0]
    alternative = speech_transcription.alternatives[0]

    print('Transcript: {}'.format(alternative.transcript))
    print('Confidence: {}\n'.format(alternative.confidence))

    print('Word level information:')
    for word_info in alternative.words:
        word = word_info.word
        start_time = word_info.start_time
        end_time = word_info.end_time
        print('\t{}s - {}s: {}'.format(
            start_time.seconds + start_time.nanos * 1e-9,
            end_time.seconds + end_time.nanos * 1e-9,
            word))
# [END video_speech_transcription]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')
    analyze_faces_parser = subparsers.add_parser(
        'boxes', help=face_bounding_boxes.__doc__)
    analyze_faces_parser.add_argument('gcs_uri')

    analyze_emotions_parser = subparsers.add_parser(
        'emotions', help=face_emotions.__doc__)
    analyze_emotions_parser.add_argument('gcs_uri')

    speech_transcription_parser = subparsers.add_parser(
        'transcription', help=speech_transcription.__doc__)
    speech_transcription_parser.add_argument('gcs_uri')

    args = parser.parse_args()

    if args.command == 'boxes':
        face_bounding_boxes(args.gcs_uri)
    elif args.command == 'emotions':
        face_emotions(args.gcs_uri)
    elif args.command == 'transcription':
        speech_transcription(args.gcs_uri)
