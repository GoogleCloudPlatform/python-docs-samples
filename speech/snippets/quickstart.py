#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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


def run_quickstart():
    # [START speech_quickstart]
    import io
    import os

    # Imports the Google Cloud client library
    from google.cloud import speech

    # Instantiates a client
    speech_client = speech.Client()

    # The name of the audio file to transcribe
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'audio.raw')

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio_sample = speech_client.sample(
            content,
            source_uri=None,
            encoding='LINEAR16',
            sample_rate=16000)

    # Detects speech in the audio file
    alternatives = speech_client.speech_api.sync_recognize(audio_sample)

    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))
    # [END speech_quickstart]


if __name__ == '__main__':
    run_quickstart()
