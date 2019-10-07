#!/usr/bin/env python

# Copyright 2019 Google Inc. All Rights Reserved.
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

"""Google Cloud Speech API sample that demonstrates using DLP
to automatically discover and redact sensitve data.

Example usage:
    python transcribe_dlp.py deidentify -p <project_id>
    python transcribe_dlp.py deidentify
                            -f './resources/sallybrown.flac' -p <project_id>
"""

import argparse
import io
import re

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud import dlp
from google.cloud.speech import enums
from google.cloud.speech import types


def deidentify(file_name, project_id):
    """ Convert speech to text and then de-identify entities using DLP. """
    # Instantiates a client
    speech_client = speech.SpeechClient()

    dlp_client = dlp.DlpServiceClient()

    parent = dlp_client.project_path(project_id)

    # Prepare info_types by converting the list of strings into a list of
    info_types = ['ALL_BASIC']
    # dictionaries (protos are also accepted).
    inspect_config = {
        'info_types': [{'name': info_type} for info_type in info_types]
    }
    # Construct deidentify configuration dictionary
    deidentify_config = {
        'info_type_transformations': {
            'transformations': [
                {
                    'primitive_transformation': {
                        'replace_with_info_type_config': {

                        }
                    }
                }
            ]
        }
    }

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US')

    # Detects speech in the audio file
    response = speech_client.recognize(config, audio)

    transcript = ''

    for result in response.results:
        transcript = '{}{}'.format(
            transcript, result.alternatives[0].transcript)

    print('Original Transcript: {}'.format(transcript))

    # Check transcription for email address,
    # since speech API returns " at " instead of "@"
    # Format with regex before sending to DLP api
    # Currently social security numbers and credit card numbers
    # are interpreted as phone numbers

    regex = (
             r".([A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`"
             r"{|}~-]+)*)(\sat\s+)((?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+"
             r"[a-z0-9](?:[a-z0-9-]*[a-z0-9]))"
    )

    updated_transcript = re.sub(regex, r" \1@\3", transcript)

    print('Email addresses reformatted: {}'.format(updated_transcript))

    # Construct item
    item = {'value': updated_transcript}

    # Call the API
    dlp_response = dlp_client.deidentify_content(
        parent, inspect_config=inspect_config,
        deidentify_config=deidentify_config, item=item)

    # Print out the results.
    print('Final Result with sensitive content redacted: {}'
          .format(dlp_response.item.value))
    # [END dlp_deidentify_masking]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'command',
        help='deidentify : replace sensitive data with [INFO TYPE]'
    parser.add_argument(
        '-f',
        '--filename',
        dest='filename',
        required=False,
        default='./resources/sallybrown.flac',
        help='speech file to transcribe and then auto-redact')
    parser.add_argument(
        '-p',
        '--project_id',
        dest='project_id',
        required=True,
        help='the name of your Google API project ID')
    args = parser.parse_args()

    if args.command == 'deidentify':
        deidentify(args.filename, args.project_id)
