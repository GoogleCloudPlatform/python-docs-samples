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
    from google.cloud.speech import enums
    from google.cloud.speech import SpeechClient
    from google.cloud.speech import types

    # Instantiates a client
    client = SpeechClient()

    # The name of the audio file to transcribe
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'audio.raw')

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
        sample_rate_hertz = 16000
        language_code = 'en-US'
        config = types.RecognitionConfig(
            encoding=encoding,
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code)

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    alternatives = response.results[0].alternatives

    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))
    # [END speech_quickstart]


if __name__ == '__main__':
    run_quickstart()
