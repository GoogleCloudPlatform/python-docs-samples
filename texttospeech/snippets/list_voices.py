#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
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

"""Google Cloud Text-To-Speech API sample application.

Example usage:
    python list_voices.py
"""


# [START tts_list_voices]
def list_voices():
    """Lists the available voices."""
    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices()

    for voice in voices.voices:
        # Display the voice's name. Example: tpc-vocoded
        print('Name: {}'.format(voice.name))

        # Display the supported language codes for this voice. Example: "en-US"
        for language_code in voice.language_codes:
            print('Supported language: {}'.format(language_code))

        # SSML Voice Gender values from google.cloud.texttospeech.enums
        ssml_voice_genders = ['SSML_VOICE_GENDER_UNSPECIFIED', 'MALE',
                              'FEMALE', 'NEUTRAL']

        # Display the SSML Voice Gender
        print('SSML Voice Gender: {}'.format(
            ssml_voice_genders[voice.ssml_gender]))

        # Display the natural sample rate hertz for this voice. Example: 24000
        print('Natural Sample Rate Hertz: {}\n'.format(
            voice.natural_sample_rate_hertz))
# [END tts_list_voices]


if __name__ == '__main__':
    list_voices()
