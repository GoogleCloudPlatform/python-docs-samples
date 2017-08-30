#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample that demonstrates how to set audio
metadata parameters.

Example usage:
    python transcribe_with_metadata.py resources/Google_Gnome.wav
    python transcribe_with_metadata.py \
        gs://cloud-samples-tests/speech/Google_Gnome.wav
"""

import argparse


# [START def_transcribe_file_with_metadata]
def transcribe_file_with_metadata(speech_file):
    """Transcribe the given audio file synchronously with
    video as the original media type."""
    from google.cloud import speech_v1_1beta1
    from google.cloud.speech_v1_1beta1 import types
    from google.cloud.speech_v1_1beta1 import enums
    client = speech_v1_1beta1.SpeechClient()

    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)

    # This shows some available metadata parameters.
    metadata = types.RecognitionMetadata(
        audio_topic='electronics',
        interaction_type=(enums.RecognitionMetadata.
                          InteractionType.DISCUSSION),
        microphone_distance=(enums.RecognitionMetadata.
                             MicrophoneDistance.MIDFIELD),
        number_of_speakers=(enums.RecognitionMetadata.
                            NumberOfSpeakers.MULTIPLE_SPEAKERS),
        original_media_type=(enums.RecognitionMetadata.
                             OriginalMediaType.VIDEO),
        recording_device_type=(enums.RecognitionMetadata.
                               RecordingDeviceType.OTHER_OUTDOOR_DEVICE))

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        metadata=metadata)

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print('Transcript: {}'.format(alternative.transcript))
# [END def_transcribe_file_with_metadata]


def transcribe_gcs_with_metadata(gcs_uri):
    """Transcribe the given audio file asynchronously with
    video as the original media type."""
    from google.cloud import speech_v1_1beta1
    from google.cloud.speech_v1_1beta1 import types
    from google.cloud.speech_v1_1beta1 import enums
    client = speech_v1_1beta1.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)

    # This shows some available metadata parameters.
    metadata = types.RecognitionMetadata(
        audio_topic='electronics',
        interaction_type=(enums.RecognitionMetadata.
                          InteractionType.DISCUSSION),
        microphone_distance=(enums.RecognitionMetadata.
                             MicrophoneDistance.MIDFIELD),
        number_of_speakers=(enums.RecognitionMetadata.
                            NumberOfSpeakers.MULTIPLE_SPEAKERS),
        original_media_type=(enums.RecognitionMetadata.
                             OriginalMediaType.VIDEO),
        recording_device_type=(enums.RecognitionMetadata.
                               RecordingDeviceType.OTHER_OUTDOOR_DEVICE))

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        metadata=metadata)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print('Transcript: {}'.format(alternative.transcript))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs_with_metadata(args.path)
    else:
        transcribe_file_with_metadata(args.path)
