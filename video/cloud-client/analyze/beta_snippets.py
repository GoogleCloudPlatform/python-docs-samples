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
    python beta_snippets.py \
    transcription gs://python-docs-samples-tests/video/googlework_short.mp4
"""

import argparse

from google.cloud import videointelligence_v1p1beta1 as videointelligence


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

    speech_transcription_parser = subparsers.add_parser(
        'transcription', help=speech_transcription.__doc__)
    speech_transcription_parser.add_argument('gcs_uri')

    args = parser.parse_args()

    if args.command == 'transcription':
        speech_transcription(args.gcs_uri)
