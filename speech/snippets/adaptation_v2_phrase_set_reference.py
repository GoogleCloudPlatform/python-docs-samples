# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

# [START speech_adaptation_v2_phrase_set_reference]
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def adaptation_v2_phrase_set_reference(
    phrase_set_id: str,
) -> cloud_speech.RecognizeResponse:
    """Transcribe audio files using a PhraseSet.

    Args:
        phrase_set_id: The unique ID of the PhraseSet to use.

    Returns:
        cloud_speech.RecognizeResponse: The full response object which includes the transcription results.
    """
    # Could be any another absolute|relative local path to the audio file
    audio_file = "resources/fair.wav"
    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        audio_content = f.read()

    # Instantiates a client
    client = SpeechClient()
    # Creating operation of creating the PhraseSet on the cloud.
    operation = client.create_phrase_set(
        parent=f"projects/{PROJECT_ID}/locations/global",
        phrase_set_id=phrase_set_id,
        phrase_set=cloud_speech.PhraseSet(phrases=[{"value": "fare", "boost": 10}]),
    )
    phrase_set = operation.result()

    # Add a reference of the PhraseSet into the recognition request
    adaptation = cloud_speech.SpeechAdaptation(
        phrase_sets=[
            cloud_speech.SpeechAdaptation.AdaptationPhraseSet(
                phrase_set=phrase_set.name
            )
        ]
    )
    # AutoDetectDecodingConfig is used to automatically detect the audio's encoding.
    # This simplifies the configuration by not requiring explicit encoding settings.
    # The model to use for the recognition. "short" is typically used for short utterances
    #   like commands or prompts.
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        adaptation=adaptation,
        language_codes=["en-US"],
        model="short",
    )
    #  Prepare the request which includes specifying the recognizer, configuration, and the audio content
    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/global/recognizers/_",
        config=config,
        content=audio_content,
    )
    # Transcribes the audio into text. The response contains the transcription results
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response


# [END speech_adaptation_v2_phrase_set_reference]


if __name__ == "__main__":
    phrase_set_unique_id = "phrase-set-123"
    adaptation_v2_phrase_set_reference(phrase_set_unique_id)
