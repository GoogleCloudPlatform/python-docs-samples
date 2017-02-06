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

"""Google Cloud Speech API sample application using the REST API for batch
processing.

Example usage:
    python transcribe.py resources/audio.raw
    python transcribe.py gs://cloud-samples-tests/speech/brooklyn.flac
"""

# [START import_libraries]
import argparse
import io
# [END import_libraries]


def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    # [START authenticating]
    # Application default credentials provided by env variable
    # GOOGLE_APPLICATION_CREDENTIALS
    from google.cloud import speech
    speech_client = speech.Client()
    # [END authenticating]

    # [START construct_request]
    # Loads the audio into memory
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()
        audio_sample = speech_client.sample(
            content,
            source_uri=None,
            encoding='LINEAR16',
            sample_rate=16000)
    # [END construct_request]

    # [START send_request]
    alternatives = speech_client.speech_api.sync_recognize(audio_sample)
    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))
    # [END send_request]


def transcribe_gcs(gcs_uri):
    """Transcribes the audio file specified by the gcs_uri."""
    # [START authenticating_gcs]
    # Application default credentials provided by env variable
    # GOOGLE_APPLICATION_CREDENTIALS
    from google.cloud import speech
    speech_client = speech.Client()
    # [END authenticating]

    # [START construct_request_gcs]
    audio_sample = speech_client.sample(
        None,
        source_uri=gcs_uri,
        encoding='FLAC',
        sample_rate=16000)
    # [END construct_request_gcs]

    # [START send_request_gcs]
    alternatives = speech_client.speech_api.sync_recognize(audio_sample)
    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))
    # [END send_request_gcs]


def main(path):
    """Transcribe the given audio file.
    Args:
        path: the name of the audio file.
    """
    if path.startswith('gs://'):
        transcribe_gcs(path)
    else:
        transcribe_file(path)


# [START run_application]
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    main(args.path)
    # [END run_application]
