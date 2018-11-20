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

"""This application demonstrates speech transcription using the
Google Cloud API.

Usage Examples:
    python beta_snippets.py transcription \
        gs://python-docs-samples-tests/video/googlework_short.mp4
    python beta_snippets.py video-text-gcs \
        gs://python-docs-samples-tests/video/googlework_short.mp4
    python beta_snippets.py track-objects /resources/cat.mp4
"""

import argparse
import io


def speech_transcription(input_uri):
    # [START video_speech_transcription_gcs_beta]
    """Transcribe speech from a video stored on GCS."""
    from google.cloud import videointelligence_v1p1beta1 as videointelligence

    video_client = videointelligence.VideoIntelligenceServiceClient()

    features = [videointelligence.enums.Feature.SPEECH_TRANSCRIPTION]

    config = videointelligence.types.SpeechTranscriptionConfig(
        language_code='en-US',
        enable_automatic_punctuation=True)
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
    for speech_transcription in annotation_results.speech_transcriptions:

        # The number of alternatives for each transcription is limited by
        # SpeechTranscriptionConfig.max_alternatives.
        # Each alternative is a different possible transcription
        # and has its own confidence score.
        for alternative in speech_transcription.alternatives:
            print('Alternative level information:')

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
    # [END video_speech_transcription_gcs_beta]


def video_detect_text_gcs(input_uri):
    # [START video_detect_text_gcs_beta]
    """Detect text in a video stored on GCS."""
    from google.cloud import videointelligence_v1p2beta1 as videointelligence

    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.TEXT_DETECTION]

    operation = video_client.annotate_video(
        input_uri=input_uri,
        features=features)

    print('\nProcessing video for text detection.')
    result = operation.result(timeout=300)

    # The first result is retrieved because a single video was processed.
    annotation_result = result.annotation_results[0]

    # Get only the first result
    text_annotation = annotation_result.text_annotations[0]
    print('\nText: {}'.format(text_annotation.text))

    # Get the first text segment
    text_segment = text_annotation.segments[0]
    start_time = text_segment.segment.start_time_offset
    end_time = text_segment.segment.end_time_offset
    print('start_time: {}, end_time: {}'.format(
        start_time.seconds + start_time.nanos * 1e-9,
        end_time.seconds + end_time.nanos * 1e-9))

    print('Confidence: {}'.format(text_segment.confidence))

    # Show the result for the first frame in this segment.
    frame = text_segment.frames[0]
    time_offset = frame.time_offset
    print('Time offset for the first frame: {}'.format(
        time_offset.seconds + time_offset.nanos * 1e-9))
    print('Rotated Bounding Box Vertices:')
    for vertex in frame.rotated_bounding_box.vertices:
        print('\tVertex.x: {}, Vertex.y: {}'.format(vertex.x, vertex.y))
    # [END video_detect_text_gcs_beta]
    return annotation_result.text_annotations


def video_detect_text(path):
    # [START video_detect_text_beta]
    """Detect text in a local video."""
    from google.cloud import videointelligence_v1p2beta1 as videointelligence

    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.TEXT_DETECTION]
    video_context = videointelligence.types.VideoContext()

    with io.open(path, 'rb') as file:
        input_content = file.read()

    operation = video_client.annotate_video(
        input_content=input_content,  # the bytes of the video file
        features=features,
        video_context=video_context)

    print('\nProcessing video for text detection.')
    result = operation.result(timeout=300)

    # The first result is retrieved because a single video was processed.
    annotation_result = result.annotation_results[0]

    # Get only the first result
    text_annotation = annotation_result.text_annotations[0]
    print('\nText: {}'.format(text_annotation.text))

    # Get the first text segment
    text_segment = text_annotation.segments[0]
    start_time = text_segment.segment.start_time_offset
    end_time = text_segment.segment.end_time_offset
    print('start_time: {}, end_time: {}'.format(
        start_time.seconds + start_time.nanos * 1e-9,
        end_time.seconds + end_time.nanos * 1e-9))

    print('Confidence: {}'.format(text_segment.confidence))

    # Show the result for the first frame in this segment.
    frame = text_segment.frames[0]
    time_offset = frame.time_offset
    print('Time offset for the first frame: {}'.format(
        time_offset.seconds + time_offset.nanos * 1e-9))
    print('Rotated Bounding Box Vertices:')
    for vertex in frame.rotated_bounding_box.vertices:
        print('\tVertex.x: {}, Vertex.y: {}'.format(vertex.x, vertex.y))
    # [END video_detect_text_beta]
    return annotation_result.text_annotations


def track_objects_gcs(gcs_uri):
    # [START video_object_tracking_gcs_beta]
    """Object Tracking."""
    from google.cloud import videointelligence_v1p2beta1 as videointelligence

    # It is recommended to use location_id as 'us-east1' for the best latency
    # due to different types of processors used in this region and others.
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.OBJECT_TRACKING]
    operation = video_client.annotate_video(
        input_uri=gcs_uri, features=features, location_id='us-east1')
    print('\nProcessing video for object annotations.')

    result = operation.result(timeout=300)
    print('\nFinished processing.\n')

    # The first result is retrieved because a single video was processed.
    object_annotations = result.annotation_results[0].object_annotations

    # Get only the first annotation for demo purposes.
    object_annotation = object_annotations[0]
    print('Entity description: {}'.format(
        object_annotation.entity.description))
    if object_annotation.entity.entity_id:
        print('Entity id: {}'.format(object_annotation.entity.entity_id))

    print('Segment: {}s to {}s'.format(
        object_annotation.segment.start_time_offset.seconds +
        object_annotation.segment.start_time_offset.nanos / 1e9,
        object_annotation.segment.end_time_offset.seconds +
        object_annotation.segment.end_time_offset.nanos / 1e9))

    print('Confidence: {}'.format(object_annotation.confidence))

    # Here we print only the bounding box of the first frame in this segment
    frame = object_annotation.frames[0]
    box = frame.normalized_bounding_box
    print('Time offset of the first frame: {}s'.format(
        frame.time_offset.seconds + frame.time_offset.nanos / 1e9))
    print('Bounding box position:')
    print('\tleft  : {}'.format(box.left))
    print('\ttop   : {}'.format(box.top))
    print('\tright : {}'.format(box.right))
    print('\tbottom: {}'.format(box.bottom))
    print('\n')
    # [END video_object_tracking_gcs_beta]
    return object_annotations


def track_objects(path):
    # [START video_object_tracking_beta]
    """Object Tracking."""
    from google.cloud import videointelligence_v1p2beta1 as videointelligence

    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.OBJECT_TRACKING]

    with io.open(path, 'rb') as file:
        input_content = file.read()

    # It is recommended to use location_id as 'us-east1' for the best latency
    # due to different types of processors used in this region and others.
    operation = video_client.annotate_video(
        input_content=input_content, features=features, location_id='us-east1')
    print('\nProcessing video for object annotations.')

    result = operation.result(timeout=300)
    print('\nFinished processing.\n')

    # The first result is retrieved because a single video was processed.
    object_annotations = result.annotation_results[0].object_annotations

    # Get only the first annotation for demo purposes.
    object_annotation = object_annotations[0]
    print('Entity description: {}'.format(
        object_annotation.entity.description))
    if object_annotation.entity.entity_id:
        print('Entity id: {}'.format(object_annotation.entity.entity_id))

    print('Segment: {}s to {}s'.format(
        object_annotation.segment.start_time_offset.seconds +
        object_annotation.segment.start_time_offset.nanos / 1e9,
        object_annotation.segment.end_time_offset.seconds +
        object_annotation.segment.end_time_offset.nanos / 1e9))

    print('Confidence: {}'.format(object_annotation.confidence))

    # Here we print only the bounding box of the first frame in this segment
    frame = object_annotation.frames[0]
    box = frame.normalized_bounding_box
    print('Time offset of the first frame: {}s'.format(
        frame.time_offset.seconds + frame.time_offset.nanos / 1e9))
    print('Bounding box position:')
    print('\tleft  : {}'.format(box.left))
    print('\ttop   : {}'.format(box.top))
    print('\tright : {}'.format(box.right))
    print('\tbottom: {}'.format(box.bottom))
    print('\n')
    # [END video_object_tracking_beta]
    return object_annotations


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    speech_transcription_parser = subparsers.add_parser(
        'transcription', help=speech_transcription.__doc__)
    speech_transcription_parser.add_argument('gcs_uri')

    video_text_gcs_parser = subparsers.add_parser(
        'video-text-gcs', help=video_detect_text_gcs.__doc__)
    video_text_gcs_parser.add_argument('gcs_uri')

    video_text_parser = subparsers.add_parser(
        'video-text', help=video_detect_text.__doc__)
    video_text_parser.add_argument('path')

    video_object_tracking_gcs_parser = subparsers.add_parser(
        'track-objects-gcs', help=track_objects_gcs.__doc__)
    video_object_tracking_gcs_parser.add_argument('gcs_uri')

    video_object_tracking_parser = subparsers.add_parser(
        'track-objects', help=track_objects.__doc__)
    video_object_tracking_parser.add_argument('path')

    args = parser.parse_args()

    if args.command == 'transcription':
        speech_transcription(args.gcs_uri)
    elif args.command == 'video-text-gcs':
        video_detect_text_gcs(args.gcs_uri)
    elif args.command == 'video-text':
        video_detect_text(args.path)
    elif args.command == 'track-objects-gcs':
        track_objects_gcs(args.gcs_uri)
    elif args.command == 'track-objects':
        track_objects(args.path)
