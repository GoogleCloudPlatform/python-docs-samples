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

"""Google Cloud Speech API sample that demonstrates automatic punctuation.

Example usage:
    python transcribe_automatic_punctuation.py resources/audio.raw
    python transcribe_automatic_punctuation.py \
        gs://cloud-samples-tests/speech/vr.flac
"""

import argparse
import io


# [START def_transcribe_file_with_automatic_punctuation]
def transcribe_file_with_automatic_punctuation(speech_file):
    """Transcribe the given audio file synchronously with automatic
    punctuation."""
    from google.cloud import speech_v1_1beta1
    from google.cloud.speech_v1_1beta1 import types
    from google.cloud.speech_v1_1beta1 import enums
    client = speech_v1_1beta1.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_automatic_punctuation=True)

    response = client.recognize(config, audio)

    alternatives = response.results[0].alternatives

    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))
# [END def_transcribe_file_with_automatic_punctuation]


def transcribe_gcs_with_automatic_punctuation(gcs_uri):
    """Transcribe the given audio file asynchronously with automatic
    punctuation."""
    from google.cloud import speech_v1_1beta1
    from google.cloud.speech_v1_1beta1 import types
    from google.cloud.speech_v1_1beta1 import enums
    client = speech_v1_1beta1.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_automatic_punctuation=True)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    result = operation.result(timeout=90)

    alternatives = result.results[0].alternatives

    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs_with_automatic_punctuation(args.path)
    else:
        transcribe_file_with_automatic_punctuation(args.path)
