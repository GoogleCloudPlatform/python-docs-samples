# Copyright 2024 Google LLC
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

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
RESOURCES_FOLDER = os.path.join(os.path.dirname(__file__), "resources")
# [START speech_adaptation_v2_custom_class_reference]
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def adaptation_v2_custom_class_reference(
    phrase_set_id: str,
    custom_class_id: str
) -> cloud_speech.RecognizeResponse:
    """Transcribe audio file using a custom class.

    Args:
        phrase_set_id: The unique ID of the phrase set to use.
        custom_class_id: The unique ID of the custom class to use.

    Returns:
        cloud_speech.RecognizeResponse: The full response object which includes the transcription results.
    """
    # Could be "resources/fair.wav" or any another absolute|relative local path to the audio file
    audio_file = os.path.join(RESOURCES_FOLDER, "fair.wav")
    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        audio_content = f.read()

    # Instantiates a speech client
    client = SpeechClient()

    # Create a custom class to reference in a PhraseSet
    # Simplified version of creating a persistent CustomClass for phrase reference
    # The CustomClass is created with a specific value ("fare") that can be used
    # to improve recognition accuracy for specific terms.
    created_custom_class = cloud_speech.CustomClass(items=[{"value": "fare"}])
    operation = client.create_custom_class(
        parent=f"projects/{PROJECT_ID}/locations/global",
        custom_class_id=custom_class_id,
        custom_class=created_custom_class,
    )
    custom_class = operation.result()

    # Create a persistent PhraseSet to reference in a recognition request
    created_phrase_set = cloud_speech.PhraseSet(
        phrases=[
            {
                "value": f"${{{custom_class.name}}}",
                "boost": 20,
            },  # Using custom class reference
        ]
    )
    operation = client.create_phrase_set(
        parent=f"projects/{PROJECT_ID}/locations/global",
        phrase_set_id=phrase_set_id,
        phrase_set=created_phrase_set,
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


    # Prepare the request which includes specifying the recognizer, configuration, and the audio content
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


# [END speech_adaptation_v2_custom_class_reference]


if __name__ == "__main__":
    phrase_set_unique_id = "custom-phrase-set"
    custom_class_unique_id = "custom-class-id"
    recognition_response = adaptation_v2_custom_class_reference(
        phrase_set_unique_id, custom_class_unique_id
    )
