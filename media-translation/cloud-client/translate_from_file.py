# Copyright 2020 Google LLC
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

"""Cloud Media Translation sample application.

Example usage:
    python translate_from_file.py resources/audio.raw
"""

import argparse

# [START media_translation_translate_from_file]
from google.cloud import mediatranslation


def translate_from_file(file_path='path/to/your/file'):

    client = mediatranslation.SpeechTranslationServiceClient()

    speech_config = mediatranslation.TranslateSpeechConfig(
        audio_encoding='linear16',
        source_language_code='en-US',
        target_language_code='fr-FR')

    config = mediatranslation.StreamingTranslateSpeechConfig(
        audio_config=speech_config)

    def request_generator(config, audio_file_path):

        # The first request contains the configuration.
        # Note that audio_content is explicitly set to None.
        yield mediatranslation.StreamingTranslateSpeechRequest(
            streaming_config=config, audio_content=None)

        with open(audio_file_path, 'rb') as audio:
            while True:
                chunk = audio.read(4096)
                if not chunk:
                    break
                yield mediatranslation.StreamingTranslateSpeechRequest(
                    audio_content=chunk,
                    streaming_config=config)

    requests = request_generator(config, file_path)
    responses = client.streaming_translate_speech(requests)

    for response in responses:
        # Once the transcription settles, the response contains the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        result = response.result
        translation = result.text_translation_result.translation
        source = result.recognition_result

        if result.text_translation_result.is_final:
            print(u'\nFinal translation: {0}'.format(translation))
            print(u'Final recognition result: {0}'.format(source))
            break

        print(u'\nPartial translation: {0}'.format(translation))
        print(u'Partial recognition result: {0}'.format(source))
    # [END media_translation_translate_from_file]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('stream', help='File to stream to the API')
    args = parser.parse_args()
    translate_from_file(args.stream)
