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

# [START mediatranslation_translate_from_file]
from google.cloud import mediatranslation


def translate_from_file(file_path="path/to/your/file"):
    client = mediatranslation.SpeechTranslationServiceClient()

    # The `sample_rate_hertz` field is not required for FLAC and WAV (Linear16)
    # encoded data. Other audio encodings must provide the sampling rate.
    audio_config = mediatranslation.TranslateSpeechConfig(
        audio_encoding="linear16",
        source_language_code="en-US",
        target_language_code="fr-FR",
    )

    streaming_config = mediatranslation.StreamingTranslateSpeechConfig(
        audio_config=audio_config, single_utterance=True
    )

    def request_generator(config, audio_file_path):

        # The first request contains the configuration.
        # Note that audio_content is explicitly set to None.
        yield mediatranslation.StreamingTranslateSpeechRequest(streaming_config=config)

        with open(audio_file_path, "rb") as audio:
            while True:
                chunk = audio.read(4096)
                if not chunk:
                    break
                yield mediatranslation.StreamingTranslateSpeechRequest(
                    audio_content=chunk
                )

    requests = request_generator(streaming_config, file_path)
    responses = client.streaming_translate_speech(requests)

    for response in responses:
        # Once the transcription settles, the response contains the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        print(f"Response: {response}")
        result = response.result
        translation = result.text_translation_result.translation

        if result.text_translation_result.is_final:
            print(f"\nFinal translation: {translation}")
            break

        print(f"\nPartial translation: {translation}")
    # [END mediatranslation_translate_from_file]
